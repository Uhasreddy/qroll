# Screenshots: practical demonstration (17 Nov 2026, Region ap-southeast-2)

| File | Shows |
|---|---|
| `01-s3-bucket-objects.jpg` | S3 bucket `tool-explorer-ra2311003010363` with the 3 uploaded files |
| `02-s3-website-endpoint.jpg` | Properties → Static website hosting: Enabled, with the website endpoint |
| `03-s3-site-live.jpg` | The website loaded from the S3 endpoint |
| `04-s3-error-page.jpg` | Custom `error.html` returned for a missing page (HTTP 404) |
| `05-ec2-instance-running.jpg` | EC2 instance `tool-explorer-web` (t3.micro) in Running state with public IP |
| `06-ec2-security-group.jpg` | Security group inbound rules: SSH (22) and HTTP (80) |
| `07-ec2-site-live.jpg` | Apache page served by the EC2 instance (instance ID, type, AZ) |

Full write-up: [docs/03-practical-demonstration.md](../docs/03-practical-demonstration.md)
