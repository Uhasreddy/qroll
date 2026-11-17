# 1. Tool Introduction — *1 mark*

## The platform: Amazon Web Services (AWS)
AWS is Amazon's public cloud, launched in 2006. It offers 200+ on-demand services billed pay-as-you-go and is the largest cloud provider by market share (Unit V). This case study uses the **serverless** part of AWS: services where AWS runs, patches and scales the servers and the customer supplies only code and data.

| Service | What it is | Role in QRoll |
|---|---|---|
| **AWS Lambda** | Runs code on demand. No server to manage; billed per request and per millisecond | The entire backend: one Python 3.12 function, `qroll-api`, handling 6 routes |
| **Amazon API Gateway (HTTP API)** | Managed HTTPS front door for APIs | Public HTTPS endpoint with CORS, routing and throttling (10 req/s, burst 20) |
| **Amazon DynamoDB** | Fully managed NoSQL key-value database | Stores events and check-ins. Conditional writes, transactions and TTL |
| **Amazon S3** | Object storage with static website hosting | Hosts the HTML/CSS/JS pages |
| **AWS IAM** | Identity and access management | Lambda's role can touch **only** this table and its own logs |
| **Amazon CloudWatch** | Logs and metrics | Invocation count, duration and error rate for the demo |

## Why serverless matters in cloud computing
- It goes further than IaaS. On EC2 you still patch the OS and pay for idle hours. With Lambda you pay **only when a request arrives**.
- It shows the cloud characteristics from Unit I directly: **on-demand self-service**, **rapid elasticity** (Lambda scales per request), **measured service** (per-request billing in CloudWatch), and **resource pooling** (thousands of customers share the same Lambda fleet).
- It is how modern apps are built: Netflix, Coca-Cola and iRobot run serverless workloads on Lambda.

## The case: why attendance?
Taking attendance by passing a sheet around wastes 5–10 minutes of a lecture. It is easy to fake ("proxy"), and someone still has to type it into a spreadsheet. A plain Google Form doesn't fix proxies, because the link can be forwarded.

**Case question:** *Can a fully serverless app take attendance faster than paper, stop forwarded-link proxies and duplicates, and cost almost nothing to run?*

QRoll answers this with a live deployment. See [03-practical-demonstration.md](03-practical-demonstration.md).
