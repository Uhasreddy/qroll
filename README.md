# ☁️ Tool Explorer: Amazon Web Services (AWS)

**Course:** 21CSE362T – Cloud Computing
**Activity:** Tool Explorer (10 marks)
**Selected tool:** Amazon Web Services (AWS)

This repository holds my Tool Explorer submission. I picked **AWS**, the leading public cloud platform (covered in Unit V, *Cloud Computing Applications: Amazon, Microsoft, Google*). The repo contains the written report, a working practical demo (a static website hosted on **Amazon S3** and on an **Amazon EC2** virtual machine), and the presentation.

---

## 📁 Repository structure

```
aws-tool-explorer/
├── README.md                         ← you are here (overview + marks map)
├── docs/
│   ├── 01-tool-introduction.md       ← Activity 1 (1 mark)
│   ├── 02-service-exploration.md     ← Activity 2 (2 marks)
│   ├── 03-practical-demonstration.md ← Activity 3 (2 marks)
│   ├── 04-feature-identification.md  ← Activity 4 (2 marks)
│   └── 05-real-time-application.md   ← Activity 5 (1 mark)
├── demo/
│   ├── website/                      ← the site deployed in the demo
│   │   ├── index.html
│   │   ├── error.html
│   │   └── style.css
│   └── scripts/
│       ├── deploy-s3-website.sh      ← Demo A: S3 static website (AWS CLI)
│       ├── bucket-policy.json
│       ├── launch-ec2-webserver.sh   ← Demo B: EC2 web server (AWS CLI)
│       ├── ec2-user-data.sh          ← boot script that installs Apache
│       └── cleanup.sh                ← deletes everything (avoid charges)
├── screenshots/                      ← add console screenshots here
└── PPT/
    └── AWS_Tool_Explorer_Presentation/
        ├── AWS_Tool_Explorer.pptx    ← presentation for the activity
        └── build_ppt.py              ← script that generated the deck
```

---

## 🧭 Marks map

| # | Activity | Marks | Where |
|---|----------|:-----:|-------|
| 1 | Tool Introduction | 1 | [docs/01-tool-introduction.md](docs/01-tool-introduction.md) |
| 2 | Service Exploration (IaaS / PaaS / SaaS) | 2 | [docs/02-service-exploration.md](docs/02-service-exploration.md) |
| 3 | Practical Demonstration | 2 | [docs/03-practical-demonstration.md](docs/03-practical-demonstration.md) + [demo/](demo/) |
| 4 | Feature Identification | 2 | [docs/04-feature-identification.md](docs/04-feature-identification.md) |
| 5 | Real-Time Application | 1 | [docs/05-real-time-application.md](docs/05-real-time-application.md) |
| — | Presentation | — | [PPT/AWS_Tool_Explorer_Presentation/](PPT/AWS_Tool_Explorer_Presentation/) |

---

## ⚡ Quick summary

- **What:** AWS is Amazon's cloud platform, launched in 2006. It offers 200+ on-demand services (compute, storage, databases, networking, AI/ML) on a **pay-as-you-go** model.
- **Service models:** IaaS (**EC2**, **S3**, **VPC**), PaaS (**Elastic Beanstalk**, **RDS**, **Lambda**), SaaS (**Amazon WorkMail**, **Amazon Chime**, **QuickSight**).
- **Demo:** (A) host a static website on **S3**, and (B) launch an **EC2** Linux VM that installs Apache through a *user-data* script and serves the same site. Both use the AWS Management Console *and* the AWS CLI.
- **Real-world use case:** **Netflix** streams to 200M+ members on AWS (EC2 Auto Scaling, S3, CloudFront, DynamoDB).

## ✅ Demo results (run on a real AWS account)

- **Live S3 website:** <http://tool-explorer-ra2311003010363.s3-website.ap-southeast-2.amazonaws.com>
- **EC2 web server:** `t3.micro` instance served the Apache page at its public IP. It was terminated after the demo to avoid charges.
- Screenshots of every step are in [`screenshots/`](screenshots/), and the results table is in [docs/03-practical-demonstration.md](docs/03-practical-demonstration.md#actual-run-17-nov-2026).

![EC2 live page](screenshots/07-ec2-site-live.jpg)

## ▶️ Run the demo yourself

Prerequisites: an AWS account (Free Tier is enough), the [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), and `aws configure` done with an IAM user's access key.

```bash
cd demo/scripts
./deploy-s3-website.sh my-unique-bucket-name-123      # Demo A → prints the website URL
./launch-ec2-webserver.sh                              # Demo B → prints http://<public-ip>
./cleanup.sh my-unique-bucket-name-123                 # delete everything afterwards
```

The full click-by-click console steps are in [docs/03-practical-demonstration.md](docs/03-practical-demonstration.md).

## 🔗 Syllabus mapping

| Unit | Topic | How this project uses it |
|------|-------|--------------------------|
| I | Cloud types, characteristics, benefits, TCO, SLA | Public cloud, pay-as-you-go, AWS SLAs (99.99% EC2) |
| II | Cloud stack, IaaS / PaaS / SaaS | AWS services classified by model |
| III | Cloud security, identity standards | IAM users/roles, security groups, shared responsibility model |
| IV | Virtualization, hypervisors, load balancing, VM imaging | EC2 on the Nitro hypervisor, AMIs, Elastic Load Balancing |
| V | Cloud applications: Amazon, Microsoft, Google | AWS platform, comparison with Azure & GCP, case studies |
