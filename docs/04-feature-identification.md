# 4. Feature Identification: Features, Benefits and Applications — *2 Marks*

## A. Important features of AWS
| # | Feature | Explanation | AWS services |
|---|---|---|---|
| 1 | **Elasticity & Auto Scaling** | Automatically adds or removes instances as load changes | EC2 Auto Scaling, Lambda |
| 2 | **Pay-as-you-go pricing** | Billed per second/request. Options: On-Demand, Reserved, Savings Plans, Spot (up to 90% cheaper) | Billing, Cost Explorer |
| 3 | **Global infrastructure** | Regions, Availability Zones, Edge Locations give low latency and fault tolerance | CloudFront, Route 53 |
| 4 | **High availability & durability** | Multi-AZ deployments; S3 has 11-nines durability | RDS Multi-AZ, S3 |
| 5 | **Load balancing** | Spreads traffic across healthy instances (Unit IV) | Elastic Load Balancing (ALB, NLB) |
| 6 | **Virtualization** | VMs on the Nitro hypervisor; AMIs as reusable machine images (Unit IV) | EC2, AMI |
| 7 | **Security & identity** | IAM users, roles, policies, MFA, encryption at rest/in transit, shared responsibility model (Unit III) | IAM, KMS, Shield, WAF |
| 8 | **Monitoring & auditing** | Metrics, logs, alarms; record of every API call | CloudWatch, CloudTrail |
| 9 | **Serverless computing** | Run code with no servers to manage | Lambda, API Gateway, DynamoDB |
| 10 | **Infrastructure as Code** | Define whole environments in templates | CloudFormation, CDK |
| 11 | **Wide service catalogue** | 200+ services incl. AI/ML, IoT, analytics | SageMaker, Bedrock, IoT Core |
| 12 | **Hybrid & migration support** | Connect or move on-premise systems (Unit IV: *Porting Applications*) | Direct Connect, Migration Hub, Outposts |

## B. Benefits
1. **Lower cost / better TCO:** no capital expenditure on servers, cooling or buildings; pay only for use (Unit I).
2. **Speed & agility:** new resources in minutes instead of weeks.
3. **Scalability:** handle sudden spikes (sales, exam results) automatically.
4. **Reliability:** multi-AZ redundancy and published SLAs (e.g. EC2 99.99%).
5. **Security & compliance:** ISO 27001, SOC 1/2/3, PCI-DSS, HIPAA certifications.
6. **Global reach:** deploy worldwide in a few clicks.
7. **Focus on business:** AWS handles undifferentiated heavy lifting such as hardware, patching and backups.
8. **Free Tier:** students can learn for free (750 hours/month of t2/t3.micro for 12 months, 5 GB S3).

## C. Limitations
- Costs can grow without monitoring (set **Budgets** and alerts).
- Vendor lock-in with proprietary services.
- The large number of services makes it hard to learn at first.
- Depends on Internet connectivity.

## D. Applications
| Domain | Application | Services used |
|---|---|---|
| Web & mobile | Hosting websites, APIs, mobile back-ends | EC2, S3, Amplify, API Gateway |
| Media streaming | Video-on-demand, live streaming | S3, CloudFront, Elemental MediaConvert |
| E-commerce | Scalable online stores | EC2 Auto Scaling, RDS, DynamoDB |
| Big data & analytics | Data lakes, BI dashboards | S3, EMR, Athena, Redshift, QuickSight |
| AI / ML | Recommendation engines, chatbots, image recognition | SageMaker, Rekognition, Lex, Bedrock |
| Backup & DR | Off-site backup, disaster recovery | S3 Glacier, AWS Backup |
| IoT | Smart devices, sensors | IoT Core, Kinesis |
| Education | Online learning platforms | EC2, S3, CloudFront (e.g. Coursera) |
| Healthcare | Secure patient data, genomics | HealthLake, S3, HIPAA-eligible services |
