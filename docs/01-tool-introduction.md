# 1. Tool Introduction: Amazon Web Services (AWS) — *1 Mark*

## What is AWS?
**Amazon Web Services (AWS)** is the public cloud platform from Amazon.com. It launched in **2006** with Amazon S3 (storage) and Amazon EC2 (compute). It now offers **200+ fully featured services** for computing, storage, networking, databases, analytics, machine learning, IoT and security, all delivered over the Internet **on demand** with **pay-as-you-go** pricing.

In simple words: instead of buying and maintaining physical servers, an organisation *rents* servers, storage and software from AWS, uses them for as long as it needs, and pays only for what it uses. It works like an electricity grid, which is the analogy used in Unit I.

## Purpose of AWS
| Purpose | Explanation |
|---------|-------------|
| Replace on-premise data centres | Rent virtual servers (EC2) and storage (S3) instead of buying hardware. |
| Turn CapEx into OpEx | No upfront capital expenditure; you pay monthly operating cost (Unit I: *Capital Expenditures, TCO*). |
| Scale on demand | Add or remove capacity in minutes (rapid elasticity). |
| Go global | Deploy close to users in many Regions around the world. |
| Speed up innovation | Ready-made managed services (databases, AI, analytics) let teams build faster. |

## Global infrastructure
- **Regions:** separate geographic areas (e.g., *Asia Pacific (Mumbai) ap-south-1*, *US East (N. Virginia) us-east-1*).
- **Availability Zones (AZs):** one or more isolated data centres inside each Region, linked by low-latency networking. They provide fault tolerance.
- **Edge Locations:** 400+ points of presence used by CloudFront (CDN) to cache content near users.
- Per the Unit V material, AWS runs **200+ data centres** with a strong presence in Northern Virginia, Oregon and Frankfurt.

## Importance of AWS in cloud computing
1. **Market leader:** AWS holds the largest share of the cloud market (about one-third). Together AWS, Azure and GCP make up most of the market (Unit V).
2. **Pioneer:** AWS made IaaS mainstream and set the model other providers follow.
3. **Shows every NIST characteristic:** on-demand self-service, broad network access, resource pooling, rapid elasticity and measured service.
4. **Covers every service model:** IaaS, PaaS and SaaS (see [Activity 2](02-service-exploration.md)).
5. **Trusted by industry:** Netflix, Airbnb, Coursera, Expedia, Formula 1, Coca-Cola, Lyft and the US FDA all run on AWS (Unit V).
6. **Reliability:** SLAs such as **99.99%** availability for EC2 Regions and **99.999999999% (11 nines) durability** for S3.

## Ways to access AWS
- **AWS Management Console:** web-based GUI.
- **AWS CLI:** command-line tool (`aws ec2 run-instances ...`).
- **SDKs:** Python (boto3), Java, JavaScript and others.
- **Infrastructure as Code:** AWS CloudFormation, AWS CDK.
