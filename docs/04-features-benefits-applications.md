# 4. Features, Benefits and Applications — *2 marks*

## 4.1 Features (and the AWS feature behind each)

| # | QRoll feature | AWS capability used |
|---|---|---|
| 1 | **Rotating QR (anti-proxy)**: token changes every 30 s and expires in 2 min | Lambda computes `HMAC-SHA256(secret, time-window)`; the secret lives only in DynamoDB |
| 2 | **No duplicate check-ins** | DynamoDB **conditional write** `attribute_not_exists(SK)` |
| 3 | **Atomic check-in**: the attendee is saved only if the event is still open, and the counter updates in the same step | DynamoDB **TransactWriteItems** (ACID across two items) |
| 4 | **Live dashboard** with flashing new rows and a counter | API Gateway + Lambda + DynamoDB `Query` (single-table design) |
| 5 | **Time-boxed sessions** plus a manual *Close check-in* | Condition `closed = false AND closesAt > now` inside the transaction |
| 6 | **CSV export** | Generated in the browser from the API response |
| 7 | **Automatic data expiry** after 7 days | DynamoDB **TTL** (free deletes) |
| 8 | **Scales automatically** | Lambda concurrency + DynamoDB on-demand capacity |
| 9 | **Monitoring** | CloudWatch Logs (7-day retention) and metrics: invocations, duration, errors |
| 10 | **One-command deploy and teardown** | AWS CLI scripts (Infrastructure as Code style) |

## 4.2 Security controls (Unit III)

| Threat | Control |
|---|---|
| Proxy via forwarded QR photo | Rotating HMAC token, 2-minute validity |
| Guessing a token | 40-bit token from a 256-bit secret; API throttled to 10 req/s |
| Reading the attendee list without permission | Organizer PIN required; stored as **PBKDF2-SHA256 (100k rounds) + random salt**; compared in constant time |
| Lambda over-privilege | IAM inline policy: only `GetItem/PutItem/UpdateItem/Query/ConditionCheckItem` on **one table** plus its own log group. No delete, no scan, no other tables |
| Other websites calling the API | CORS allows only the QRoll website origin |
| Script injection via names | Input validation in Lambda (length, `[A-Z0-9]{4,20}` register numbers) and HTML-escaping in the browser |
| Secrets leaking in responses | Public route returns only title, venue, status and count; never the secret or hash |
| Data kept forever | TTL deletes events and attendees 7 days after closing |

**Known limits (stated honestly):**
- One person could still check in a friend by entering the friend's register number while physically present. Fixing that needs a college SSO login or a device check.
- The S3 website endpoint is HTTP. Production would put **CloudFront + ACM** in front for HTTPS. The API itself is already HTTPS.

## 4.3 Benefits

| Benefit | Evidence from this project |
|---|---|
| **Near-zero cost** | No running servers. Idle cost is ₹0. The whole demo (≈100 requests) is far inside the free tier |
| **No server management** | No OS, patches, SSH or load balancer to configure |
| **Elastic** | The same deployment handles a 10-person lab or a 2,000-person fest; Lambda and DynamoDB scale per request |
| **Highly available** | Lambda and DynamoDB run across 3 Availability Zones in the Region by default |
| **Fast to deliver** | Full deploy in about 1 minute from one script |
| **Faster class time** | Check-in takes ~10 s per student in parallel, vs passing a sheet around for minutes |
| **Auditable** | Every check-in has a server timestamp; CloudWatch logs every request |

## 4.4 Cost estimate (AWS public pricing, approximate)
For **one college**: 50 classes/day × 60 students × 22 days ≈ **66,000 check-ins/month**, plus dashboard polling (≈ 15 polls/min × 10 min × 1,100 sessions ≈ 165,000 requests).

| Service | Usage / month | Approx. cost |
|---|---|---|
| Lambda | ~250k requests, ~30 ms each, 256 MB | within the always-free 1M requests + 400k GB-s |
| API Gateway HTTP API | ~250k requests | ≈ US$0.25 (US$1.00 per million) |
| DynamoDB on-demand | ~70k writes, ~200k reads, < 1 GB | ≈ US$0.15 |
| S3 website | a few MB, ~10k GETs | < US$0.01 |
| **Total** | | **≈ US$0.40/month** (≈ ₹35), vs a t3.small EC2 running 24×7 ≈ US$17/month |

## 4.5 Applications
| Where | How QRoll is used |
|---|---|
| College lectures and labs | Daily attendance in under a minute; CSV goes to the ERP |
| Workshops / guest lectures | Attendance-based participation certificates |
| Hackathons and fests | Entry check-in at registration desks; live headcount |
| Conferences / seminars | Session-wise attendance for CPD credits |
| Corporate training | Proof of training completion for compliance |
| Exam halls | Quick seat-presence check before the paper starts |
