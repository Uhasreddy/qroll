#!/usr/bin/env bash
# Demo B: launch a Free-Tier EC2 instance that installs Apache on boot.
# Usage: ./launch-ec2-webserver.sh [region]
set -euo pipefail

REGION="${1:-ap-south-1}"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="tool-explorer-web"
KEY="tool-explorer-key"
SG="tool-explorer-sg"
export AWS_DEFAULT_REGION="$REGION"

echo "==> 1. Finding the latest Amazon Linux 2023 AMI"
AMI=$(aws ssm get-parameters \
  --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query 'Parameters[0].Value' --output text)
echo "    AMI: $AMI"

echo "==> 2. Creating key pair ($KEY.pem)"
if [ ! -f "$HERE/$KEY.pem" ]; then
  aws ec2 create-key-pair --key-name "$KEY" --query KeyMaterial --output text > "$HERE/$KEY.pem"
  chmod 400 "$HERE/$KEY.pem"
fi

echo "==> 3. Creating security group (virtual firewall) in the default VPC"
VPC=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)
SG_ID=$(aws ec2 create-security-group --group-name "$SG" \
  --description "Tool Explorer: SSH + HTTP" --vpc-id "$VPC" --query GroupId --output text)
MY_IP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr "$MY_IP/32" >/dev/null
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80 --cidr 0.0.0.0/0 >/dev/null
echo "    Security group: $SG_ID (22 from $MY_IP, 80 from anywhere)"

echo "==> 4. Launching t3.micro instance with user data"
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI" --instance-type t3.micro \
  --key-name "$KEY" --security-group-ids "$SG_ID" \
  --user-data "file://$HERE/ec2-user-data.sh" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NAME}]" \
  --query 'Instances[0].InstanceId' --output text)
echo "    Instance: $INSTANCE_ID"

echo "==> 5. Waiting for the instance to be running"
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo
echo "✅ Instance is running. Apache needs about 1 minute to install, then open:"
echo "   http://$IP"
echo "   SSH: ssh -i $HERE/$KEY.pem ec2-user@$IP"
