"""QRoll: serverless QR attendance API (AWS Lambda + API Gateway HTTP API + DynamoDB).

Routes (API Gateway HTTP API, payload format 2.0):
  POST /events                    create an event (organizer sets a PIN)
  GET  /events/{id}               public event info (title, venue, open/closed, count)
  GET  /events/{id}/qr            current rotating check-in token   [organizer PIN]
  POST /events/{id}/checkin       attendee check-in with token
  GET  /events/{id}/attendees     attendee list                     [organizer PIN]
  POST /events/{id}/close         close check-in early              [organizer PIN]

DynamoDB single-table design (table name from env TABLE_NAME):
  PK = "EVENT#<id>", SK = "META"          -> event item
  PK = "EVENT#<id>", SK = "ATT#<REGNO>"   -> one attendee (unique per event)
"""
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time

import boto3
from botocore.exceptions import ClientError

TABLE = os.environ["TABLE_NAME"]
TOKEN_WINDOW_SECONDS = 30      # QR token changes every 30 s
TOKEN_GRACE_WINDOWS = 4        # a scanned token stays valid for up to 2 minutes
RETENTION_DAYS = 7             # DynamoDB TTL removes event data 7 days after it closes

ddb = boto3.client("dynamodb")

REGNO_RE = re.compile(r"^[A-Z0-9]{4,20}$")
PIN_RE = re.compile(r"^\d{6,10}$")


# ---------- helpers ----------
def resp(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Cache-Control": "no-store"},
        "body": json.dumps(body),
    }


def now():
    return int(time.time())


def hash_pin(pin, salt):
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), bytes.fromhex(salt), 100_000).hex()


def token_for(secret, event_id, window):
    mac = hmac.new(bytes.fromhex(secret), f"{event_id}:{window}".encode(), hashlib.sha256).digest()
    return base64.b32encode(mac).decode()[:8]


def get_event(event_id):
    item = ddb.get_item(
        TableName=TABLE, Key={"PK": {"S": f"EVENT#{event_id}"}, "SK": {"S": "META"}}, ConsistentRead=True
    ).get("Item")
    if not item:
        return None
    return {
        "id": event_id,
        "title": item["title"]["S"],
        "venue": item["venue"]["S"],
        "createdAt": int(item["createdAt"]["N"]),
        "closesAt": int(item["closesAt"]["N"]),
        "closed": item["closed"]["BOOL"],
        "count": int(item["count"]["N"]),
        "salt": item["salt"]["S"],
        "pinHash": item["pinHash"]["S"],
        "secret": item["secret"]["S"],
    }


def public_view(ev):
    is_open = (not ev["closed"]) and now() < ev["closesAt"]
    return {k: ev[k] for k in ("id", "title", "venue", "createdAt", "closesAt", "count")} | {"open": is_open}


def organizer_ok(event, ev):
    pin = (event.get("headers") or {}).get("x-organizer-pin", "")
    return bool(PIN_RE.match(pin)) and hmac.compare_digest(hash_pin(pin, ev["salt"]), ev["pinHash"])


def body_of(event):
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode()
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


# ---------- route handlers ----------
def create_event(event):
    b = body_of(event)
    title = str(b.get("title", "")).strip()
    venue = str(b.get("venue", "")).strip()
    pin = str(b.get("pin", "")).strip()
    try:
        minutes = int(b.get("minutes", 60))
    except (TypeError, ValueError):
        minutes = 0
    if not (3 <= len(title) <= 80) or not (2 <= len(venue) <= 80):
        return resp(400, {"error": "Title (3-80 chars) and venue (2-80 chars) are required."})
    if not PIN_RE.match(pin):
        return resp(400, {"error": "Organizer PIN must be 6-10 digits."})
    if not 5 <= minutes <= 480:
        return resp(400, {"error": "Check-in duration must be 5-480 minutes."})

    event_id = secrets.token_urlsafe(6).replace("-", "x").replace("_", "y")
    salt = secrets.token_hex(16)
    created = now()
    closes = created + minutes * 60
    ddb.put_item(
        TableName=TABLE,
        Item={
            "PK": {"S": f"EVENT#{event_id}"}, "SK": {"S": "META"},
            "title": {"S": title}, "venue": {"S": venue},
            "createdAt": {"N": str(created)}, "closesAt": {"N": str(closes)},
            "closed": {"BOOL": False}, "count": {"N": "0"},
            "salt": {"S": salt}, "pinHash": {"S": hash_pin(pin, salt)},
            "secret": {"S": secrets.token_hex(32)},
            "expiresAt": {"N": str(closes + RETENTION_DAYS * 86400)},
        },
        ConditionExpression="attribute_not_exists(PK)",
    )
    return resp(201, {"id": event_id, "closesAt": closes})


def event_info(ev):
    return resp(200, public_view(ev))


def current_qr(event, ev):
    if not organizer_ok(event, ev):
        return resp(401, {"error": "Wrong organizer PIN."})
    window = now() // TOKEN_WINDOW_SECONDS
    return resp(200, {
        "token": token_for(ev["secret"], ev["id"], window),
        "refreshInSeconds": TOKEN_WINDOW_SECONDS - now() % TOKEN_WINDOW_SECONDS,
        "event": public_view(ev),
    })


def checkin(event, ev):
    b = body_of(event)
    name = " ".join(str(b.get("name", "")).split())
    reg = str(b.get("regNo", "")).strip().upper()
    token = str(b.get("token", "")).strip().upper()
    if not 2 <= len(name) <= 60:
        return resp(400, {"error": "Enter your full name."})
    if not REGNO_RE.match(reg):
        return resp(400, {"error": "Register number must be 4-20 letters/digits."})

    t = now()
    if ev["closed"] or t >= ev["closesAt"]:
        return resp(410, {"error": "Check-in for this event is closed."})

    window = t // TOKEN_WINDOW_SECONDS
    valid = {token_for(ev["secret"], ev["id"], window - i) for i in range(TOKEN_GRACE_WINDOWS)}
    if not any(hmac.compare_digest(token, v) for v in valid):
        return resp(403, {"error": "This QR code has expired. Scan the live QR on the screen again."})

    pk = {"S": f"EVENT#{ev['id']}"}
    try:
        # One atomic transaction: add the attendee only if not already present AND the
        # event is still open, and bump the counter in the same step.
        ddb.transact_write_items(TransactItems=[
            {"Put": {
                "TableName": TABLE,
                "Item": {
                    "PK": pk, "SK": {"S": f"ATT#{reg}"},
                    "name": {"S": name}, "regNo": {"S": reg},
                    "checkedInAt": {"N": str(t)},
                    "expiresAt": {"N": str(ev["closesAt"] + RETENTION_DAYS * 86400)},
                },
                "ConditionExpression": "attribute_not_exists(SK)",
            }},
            {"Update": {
                "TableName": TABLE,
                "Key": {"PK": pk, "SK": {"S": "META"}},
                "UpdateExpression": "ADD #c :one",
                "ConditionExpression": "#closed = :f AND closesAt > :now",
                "ExpressionAttributeNames": {"#c": "count", "#closed": "closed"},
                "ExpressionAttributeValues": {":one": {"N": "1"}, ":f": {"BOOL": False}, ":now": {"N": str(t)}},
            }},
        ])
    except ClientError as e:
        if e.response["Error"]["Code"] == "TransactionCanceledException":
            reasons = e.response.get("CancellationReasons", [])
            if reasons and reasons[0].get("Code") == "ConditionalCheckFailed":
                return resp(409, {"error": f"{reg} is already checked in for this event."})
            return resp(410, {"error": "Check-in for this event is closed."})
        raise
    return resp(201, {"ok": True, "name": name, "regNo": reg, "checkedInAt": t, "event": ev["title"]})


def attendees(event, ev):
    if not organizer_ok(event, ev):
        return resp(401, {"error": "Wrong organizer PIN."})
    items, kwargs = [], {
        "TableName": TABLE,
        "KeyConditionExpression": "PK = :pk AND begins_with(SK, :att)",
        "ExpressionAttributeValues": {":pk": {"S": f"EVENT#{ev['id']}"}, ":att": {"S": "ATT#"}},
    }
    while True:
        page = ddb.query(**kwargs)
        items += page["Items"]
        if "LastEvaluatedKey" not in page:
            break
        kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    rows = sorted(
        ({"name": i["name"]["S"], "regNo": i["regNo"]["S"], "checkedInAt": int(i["checkedInAt"]["N"])} for i in items),
        key=lambda r: r["checkedInAt"],
    )
    return resp(200, {"event": public_view(ev), "attendees": rows})


def close_event(event, ev):
    if not organizer_ok(event, ev):
        return resp(401, {"error": "Wrong organizer PIN."})
    ddb.update_item(
        TableName=TABLE,
        Key={"PK": {"S": f"EVENT#{ev['id']}"}, "SK": {"S": "META"}},
        UpdateExpression="SET #closed = :t",
        ExpressionAttributeNames={"#closed": "closed"},
        ExpressionAttributeValues={":t": {"BOOL": True}},
    )
    ev["closed"] = True
    return resp(200, {"event": public_view(ev)})


EVENT_ROUTES = {
    "GET /events/{id}": lambda e, ev: event_info(ev),
    "GET /events/{id}/qr": current_qr,
    "POST /events/{id}/checkin": checkin,
    "GET /events/{id}/attendees": attendees,
    "POST /events/{id}/close": close_event,
}


def lambda_handler(event, context):
    route = event.get("routeKey", "")
    try:
        if route == "POST /events":
            return create_event(event)
        if route in EVENT_ROUTES:
            event_id = (event.get("pathParameters") or {}).get("id", "")
            if not re.fullmatch(r"[A-Za-z0-9]{6,16}", event_id):
                return resp(404, {"error": "Event not found."})
            ev = get_event(event_id)
            if not ev:
                return resp(404, {"error": "Event not found."})
            return EVENT_ROUTES[route](event, ev)
        return resp(404, {"error": "Unknown route."})
    except Exception as exc:  # logged to CloudWatch, generic message to client
        print(json.dumps({"level": "error", "route": route, "error": repr(exc)}))
        return resp(500, {"error": "Server error. Please try again."})
