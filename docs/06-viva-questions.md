# 6. Viva Preparation — *2 Marks*

Short answers to likely viva questions, grouped by the rubric areas.

## A. Platform
**1. What is AWS?**
Amazon's public cloud platform (launched 2006). It offers 200+ on-demand services over the Internet with pay-as-you-go pricing.

**2. What is a Region and an Availability Zone?**
A Region is a geographic area (e.g. ap-south-1 Mumbai). An AZ is one or more isolated data centres inside a Region. Using several AZs gives fault tolerance.

**3. Which cloud deployment model is AWS?**
Public cloud. It can also form a **hybrid cloud** with on-premise systems through Direct Connect, VPN or Outposts.

**4. What are Edge Locations?**
Sites used by **CloudFront** (CDN) and Route 53 to cache content close to users and reduce latency.

**5. Who are AWS's main competitors?**
Microsoft Azure (2010) and Google Cloud Platform (2011).

## B. Services
**6. Give an example of IaaS, PaaS and SaaS on AWS.**
IaaS: EC2, S3, VPC. PaaS: Elastic Beanstalk, RDS, Lambda. SaaS: Amazon WorkMail, Chime, QuickSight.

**7. Difference between EC2 and Lambda?**
EC2 gives you a full VM that you manage and pay for while it runs. Lambda runs your function only when triggered (serverless) and charges per request/ms.

**8. Difference between S3 and EBS?**
S3 is **object** storage accessed over HTTP, with unlimited capacity. EBS is **block** storage, a virtual disk attached to one EC2 instance.

**9. What is an AMI?**
An Amazon Machine Image: a template (OS + software + settings) used to launch EC2 instances. It is an example of VM imaging (Unit IV).

**10. What is RDS?**
A managed relational database service (MySQL, PostgreSQL, Aurora, etc.). AWS handles backups, patching and Multi-AZ failover.

**11. What is Elastic Beanstalk?**
A PaaS where you upload code and AWS automatically creates the EC2 instances, load balancer, auto-scaling and monitoring.

## C. Features & security
**12. What is Auto Scaling?**
It automatically increases or decreases the number of EC2 instances based on demand (e.g. CPU > 70%). This is rapid elasticity.

**13. What is Elastic Load Balancing?**
A service that distributes incoming traffic across multiple healthy targets (EC2, containers, Lambda). Types: Application (L7), Network (L4), Gateway.

**14. What is IAM?**
Identity and Access Management. It controls *who* (users, groups, roles) can do *what* (policies) on which resources. It is free. Best practice: do not use the root user, enable MFA, and grant least privilege.

**15. What is the Shared Responsibility Model?**
AWS is responsible for security **of** the cloud (hardware, facilities, hypervisor). The customer is responsible for security **in** the cloud (OS patches, data, IAM, firewall rules).

**16. What is a Security Group?**
A stateful virtual firewall at the instance level. It allows inbound/outbound traffic by protocol, port and source.

**17. What are EC2 pricing options?**
On-Demand, Reserved Instances / Savings Plans (1–3 yr commitment, up to 72% off), Spot Instances (spare capacity, up to 90% off), Dedicated Hosts.

**18. What does CloudWatch do?**
It collects metrics and logs, creates dashboards and triggers alarms (e.g. send e-mail when CPU > 80%).

**19. Which hypervisor does EC2 use?**
The **AWS Nitro System**, which is KVM-based. Older instances used Xen.

## D. Practical demonstration
**20. What steps did you follow to host the website on S3?**
Create bucket → turn off Block Public Access → upload files → enable Static Website Hosting (index/error documents) → add a public-read bucket policy → open the website endpoint.

**21. Why did you open port 80 in the security group?**
Port 80 is HTTP. Without an inbound rule, the firewall blocks browser requests to Apache.

**22. What is user data in EC2?**
A script that runs automatically on the first boot of an instance. I used it to install and start Apache (`httpd`) and create the web page.

**23. Difference between Stop and Terminate?**
Stop shuts the VM down but keeps its EBS disk, and it can be restarted. Terminate deletes the instance permanently.

**24. How do you avoid charges after the demo?**
Terminate the EC2 instance, empty and delete the S3 bucket, delete unused key pairs/security groups, and set an AWS Budget alert.

**25. Is the S3 website HTTPS?**
No. The S3 website endpoint is HTTP only. For HTTPS, put **CloudFront** with an ACM certificate in front of it.

## E. Applications
**26. Give a real-world AWS use case.**
Netflix runs streaming on EC2 Auto Scaling, S3, ELB, DynamoDB and EMR, and survives failures using multiple AZs and chaos engineering.

**27. Which industries use AWS?**
Media (Netflix), travel (Airbnb, Expedia), education (Coursera), sports (Formula 1), finance (Coinbase), government (FDA).

**28. Why should a startup choose AWS?**
No upfront cost, Free Tier, pay-as-you-go, scales with growth, and a wide range of managed services so a small team can build quickly.
