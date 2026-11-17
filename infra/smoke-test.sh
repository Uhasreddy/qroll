#!/usr/bin/env bash
# End-to-end test against the live API: create event, fetch token, check in,
# block duplicate, reject a forged token, list attendees, close, reject late check-in.
# Usage: ./smoke-test.sh <api-url>
set -euo pipefail
API="${1:?Usage: $0 <api-url>}"
PIN=$(python3 -c "import secrets;print(secrets.randbelow(9*10**7)+10**7)")
pass=0; fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS  $1 (HTTP $3)"; pass=$((pass+1)); else echo "  FAIL  $1 (expected $2, got $3)"; fail=$((fail+1)); fi; }
req() { curl -s -o /tmp/qroll_body -w '%{http_code}' "$@"; }

code=$(req -X POST "$API/events" -H 'content-type: application/json' \
  -d "{\"title\":\"Smoke test\",\"venue\":\"Lab\",\"minutes\":5,\"pin\":\"$PIN\"}")
check "create event" 201 "$code"
ID=$(python3 -c 'import json;print(json.load(open("/tmp/qroll_body"))["id"])')

check "wrong PIN rejected"     401 "$(req "$API/events/$ID/qr" -H 'x-organizer-pin: 000000')"
check "organizer gets QR token" 200 "$(req "$API/events/$ID/qr" -H "x-organizer-pin: $PIN")"
TOKEN=$(python3 -c 'import json;print(json.load(open("/tmp/qroll_body"))["token"])')

body() { echo "{\"name\":\"$1\",\"regNo\":\"$2\",\"token\":\"$3\"}"; }
check "check-in"               201 "$(req -X POST "$API/events/$ID/checkin" -H 'content-type: application/json' -d "$(body 'Test Student' RA0000000000001 "$TOKEN")")"
check "duplicate blocked"      409 "$(req -X POST "$API/events/$ID/checkin" -H 'content-type: application/json' -d "$(body 'Test Student' RA0000000000001 "$TOKEN")")"
check "forged token rejected"  403 "$(req -X POST "$API/events/$ID/checkin" -H 'content-type: application/json' -d "$(body 'Proxy Person' RA0000000000002 ABCDEFGH)")"
check "attendee list"          200 "$(req "$API/events/$ID/attendees" -H "x-organizer-pin: $PIN")"
check "close event"            200 "$(req -X POST "$API/events/$ID/close" -H "x-organizer-pin: $PIN")"
check "late check-in rejected" 410 "$(req -X POST "$API/events/$ID/checkin" -H 'content-type: application/json' -d "$(body 'Late Comer' RA0000000000003 "$TOKEN")")"
check "unknown event"          404 "$(req "$API/events/doesnotexist")"

echo; echo "$pass passed, $fail failed"; [ "$fail" = 0 ]
