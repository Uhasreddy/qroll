# 2. Service Exploration: Mapping QRoll to IaaS / PaaS / SaaS — *2 marks*

The table classifies each service by the job it actually does in this project, not by the label a brochure gives it.

| Model | In QRoll? | Service | Why it belongs here |
|---|---|---|---|
| **IaaS** | ❌ **Not used** | (EC2 would be IaaS) | No virtual machine anywhere. Choosing *not* to rent servers is the main design decision. With EC2 we would patch Linux, keep the VM running 24×7 and pay for idle time. |
| **PaaS / FaaS** | ✅ | **AWS Lambda** | Function-as-a-Service, the serverless form of PaaS. We upload `lambda_function.py`; AWS provides the runtime, OS, scaling and availability. |
| **PaaS (managed API)** | ✅ | **Amazon API Gateway** | We declare routes, CORS and throttling; AWS runs the HTTPS infrastructure. |
| **DBaaS (managed PaaS)** | ✅ | **Amazon DynamoDB** | Database-as-a-Service. No DB server, no capacity planning (on-demand mode), automatic replication across 3 Availability Zones. |
| **Storage service** | ✅ | **Amazon S3** | Object storage that also serves our static website files over HTTP. |
| **SaaS** | ✅ (tools) | **AWS Management Console**, **CloudWatch dashboards**, **GitHub** | Finished software we only *use*: to inspect resources, read metrics and host the source code. |

> **Honest note:** QRoll itself behaves like a small **SaaS** product. An organizer opens a URL and uses it with nothing to install. Under the hood it is built on PaaS/FaaS, not IaaS.

## Who manages what (shared responsibility, Unit III)

| Layer | EC2 version (IaaS) | QRoll (serverless) |
|---|---|---|
| Physical servers, network | AWS | AWS |
| Operating system patches | **Us** | AWS |
| Runtime (Python) | **Us** | AWS |
| Scaling / load balancing | **Us** (Auto Scaling + ELB) | AWS (automatic) |
| Database server | **Us** (install MySQL) | AWS (DynamoDB) |
| Application code | Us | Us |
| Data + access rules (IAM, PIN) | Us | Us |

## Services explored with examples from this project

### AWS Lambda
- **Trigger:** API Gateway invokes the function with an *event* containing `routeKey`, path parameters, headers and body.
- **Config used:** Python 3.12, 256 MB memory, 10 s timeout, 3.6 KB code package, env var `TABLE_NAME`.
- **Cold start vs warm:** the first call took about 500 ms (cold start). Later calls took about 5–40 ms. Both are visible in the CloudWatch *Duration* graph.

### Amazon API Gateway (HTTP API)
- 6 routes, e.g. `POST /events/{id}/checkin` → Lambda proxy integration (payload v2.0).
- **CORS** allows only the S3 website's origin, so other websites cannot call the API from a browser.
- **Throttling:** 10 requests/s steady, burst 20. This protects the free-tier budget and slows brute-force attempts.

### Amazon DynamoDB
- **Single-table design:** `PK = EVENT#<id>`, `SK = META` for the event, `SK = ATT#<REGNO>` for each attendee. One `Query` returns the whole attendance list.
- **Conditional write:** `attribute_not_exists(SK)` makes a register number unique per event.
- **Transaction:** `TransactWriteItems` inserts the attendee *and* increments the counter only if the event is still open. Both happen or neither does.
- **TTL:** attribute `expiresAt`; DynamoDB deletes the data 7 days after the event closes at no cost.

### Amazon S3 static website hosting
- Bucket `qroll-ra2311003010363` with website hosting on and a public-read policy for the site files only.
- `deploy.sh` writes `config.js` with the API URL, so the same frontend works in any account.

## Comparison: the same app on other clouds (Unit V)
| QRoll piece | AWS | Microsoft Azure | Google Cloud |
|---|---|---|---|
| Functions | Lambda | Azure Functions | Cloud Run functions |
| API front door | API Gateway | API Management | API Gateway |
| NoSQL DB | DynamoDB | Cosmos DB | Firestore |
| Static site | S3 website | Blob Storage static website | Cloud Storage bucket |
