#!/usr/bin/env bash
# Delete everything created by the demos so the AWS account is not charged.
# Usage: ./cleanup.sh <bucket-name> [region]
set -uo pipefail

BUCKET="${1:-}"
REGION="${2:-ap-south-1}"
HERE="$(cd "$(dirname "$0")" && pwd)"
export AWS_DEFAULT_REGION="$REGION"

echo "==> Terminating tool-explorer-web instances"
IDS=$(aws ec2 describe-instances \
  --filters Name=tag:Name,Values=tool-explorer-web Name=instance-state-name,Values=pending,running,stopped \
  --query 'Reservations[].Instances[].InstanceId' --output text)
if [ -n "$IDS" ]; then
  aws ec2 terminate-instances --instance-ids $IDS >/dev/null
  aws ec2 wait instance-terminated --instance-ids $IDS
fi

echo "==> Deleting security group and key pair"
SG_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=tool-explorer-sg \
  --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)
[ "$SG_ID" != "None" ] && [ -n "$SG_ID" ] && aws ec2 delete-security-group --group-id "$SG_ID"
aws ec2 delete-key-pair --key-name tool-explorer-key
rm -f "$HERE/tool-explorer-key.pem"

if [ -n "$BUCKET" ]; then
  echo "==> Emptying and deleting s3://$BUCKET"
  aws s3 rb "s3://$BUCKET" --force
fi

echo "✅ Cleanup complete."
