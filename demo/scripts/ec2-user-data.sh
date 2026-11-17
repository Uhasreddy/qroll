#!/bin/bash
# EC2 user data: runs once, as root, on the instance's first boot.
# Installs Apache and publishes a page that shows which instance/AZ served it.
dnf update -y
dnf install -y httpd
systemctl enable --now httpd

# Read instance details from the EC2 Instance Metadata Service (IMDSv2)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
md() { curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/$1"; }
INSTANCE_ID=$(md instance-id)
AZ=$(md placement/availability-zone)
TYPE=$(md instance-type)

cat > /var/www/html/index.html <<EOF
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tool Explorer – EC2</title>
<style>
 body{margin:0;font-family:system-ui,Arial,sans-serif;background:#232f3e;color:#fff;display:grid;place-items:center;min-height:100vh;text-align:center;padding:16px}
 h1 span{color:#ff9900} table{margin:24px auto;border-collapse:collapse;background:#fff;color:#16191f;border-radius:8px;overflow:hidden}
 td{padding:10px 18px;border-bottom:1px solid #e5e7eb;text-align:left} td:first-child{font-weight:700;background:#fff4e0}
</style></head>
<body><div>
 <p>21CSE362T · Cloud Computing · Tool Explorer</p>
 <h1>Hello from <span>Amazon EC2</span> 👋</h1>
 <p>This page is served by Apache on a virtual machine that was created and configured automatically.</p>
 <table>
  <tr><td>Instance ID</td><td>${INSTANCE_ID}</td></tr>
  <tr><td>Instance type</td><td>${TYPE}</td></tr>
  <tr><td>Availability Zone</td><td>${AZ}</td></tr>
  <tr><td>Web server</td><td>Apache httpd (installed via user data)</td></tr>
 </table>
</div></body></html>
EOF
