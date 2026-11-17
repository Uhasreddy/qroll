# 2. Service Exploration: IaaS, PaaS and SaaS on AWS — *2 Marks*

Unit II describes the **cloud computing stack**. Each layer hides more of the infrastructure from the user:

```
        ┌──────────────────────────────┐
 SaaS   │  Ready-to-use software        │  e.g. Amazon WorkMail, Chime, QuickSight
        ├──────────────────────────────┤
 PaaS   │  Platform: runtime, DB, OS     │  e.g. Elastic Beanstalk, RDS, Lambda
        ├──────────────────────────────┤
 IaaS   │  Virtual servers, storage, net │  e.g. EC2, S3, EBS, VPC
        └──────────────────────────────┘
```

| | You manage | AWS manages |
|---|---|---|
| **IaaS** | OS, runtime, app, data | Hardware, virtualization, network |
| **PaaS** | App code and data | OS, patching, runtime, scaling |
| **SaaS** | Only your usage/data | Everything |

---

## A. Infrastructure as a Service (IaaS)

### Amazon EC2 (Elastic Compute Cloud)
- Resizable **virtual machines** (instances) running on the AWS **Nitro hypervisor** (Unit IV: *Hypervisors*).
- Instance families: *General purpose* (t3, m7), *Compute optimized* (c7), *Memory optimized* (r7), *GPU / accelerated* (p5, g5).
- Started from an **AMI (Amazon Machine Image)**, a template containing the OS and software (Unit IV: *Virtual Machine Imaging*).
- **Example:** a college runs its exam portal on two `t3.medium` instances during results week and stops them afterwards.

### Amazon S3 (Simple Storage Service)
- **Object storage**: files (objects) are stored in **buckets**, with unlimited capacity and 11-nines durability.
- Storage classes: Standard, Intelligent-Tiering, Standard-IA, Glacier (archive).
- **Example:** storing lecture videos, backups, or hosting a static website (our demo).

### Amazon EBS and Amazon VPC
- **EBS:** block storage disks attached to EC2 instances.
- **VPC (Virtual Private Cloud):** your own isolated virtual network with subnets, route tables and gateways.

---

## B. Platform as a Service (PaaS)

### AWS Elastic Beanstalk
- Upload code (Java, Python, Node.js, PHP, .NET, Go). Beanstalk then **provisions EC2, load balancer, Auto Scaling and monitoring automatically**.
- **Example:** a student uploads a Flask app `.zip` and gets a live URL without configuring servers.

### Amazon RDS (Relational Database Service)
- Managed MySQL, PostgreSQL, MariaDB, Oracle, SQL Server and Amazon Aurora. AWS handles backups, patching and replication.
- **Example:** the student-records database of a university ERP.

### AWS Lambda (serverless / FaaS)
- Run code **without managing servers**. Code runs only when triggered, and you pay per request and per millisecond.
- **Example:** when a photo is uploaded to S3, a Lambda function automatically creates a thumbnail.

---

## C. Software as a Service (SaaS)

| Service | What it is | Example |
|---|---|---|
| **Amazon WorkMail** | Managed business e-mail and calendar | Company e-mail without running a mail server |
| **Amazon Chime** | Online meetings, video, chat | Team meetings and webinars |
| **Amazon QuickSight** | Business-intelligence dashboards | Sales dashboards for managers |
| **Amazon Connect** | Cloud contact centre | Customer-support call centre |
| **AWS Marketplace** | Thousands of 3rd-party SaaS products | Buying a firewall or CRM by subscription |

---

## D. Other important service categories
| Category | Services |
|---|---|
| Networking & CDN | VPC, Route 53 (DNS), CloudFront (CDN), Elastic Load Balancing |
| Databases | DynamoDB (NoSQL), ElastiCache, Redshift (data warehouse) |
| Security & Identity | IAM, KMS, Cognito, Shield, WAF |
| Monitoring | CloudWatch, CloudTrail |
| AI / ML | SageMaker, Rekognition, Polly, Bedrock |

## E. Comparison with Azure and GCP (Unit V)
| Need | AWS | Microsoft Azure | Google Cloud |
|---|---|---|---|
| Virtual machines | EC2 | Azure Virtual Machines | Compute Engine |
| Serverless | Lambda | Azure Functions | Cloud Functions |
| Object storage | S3 | Blob Storage | Cloud Storage |
| PaaS app hosting | Elastic Beanstalk | App Service | App Engine |
| Launched | 2006 | 2010 | 2011 |
