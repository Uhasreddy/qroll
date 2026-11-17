#!/usr/bin/env bash
# Remove every QRoll resource from the AWS account (stops all charges).
# Usage: ./cleanup.sh <bucket-name> [region]
set -uo pipefail

BUCKET="${1:?Usage: $0 <bucket-name> [region]}"
REGION="${2:-ap-southeast-2}"
export AWS_DEFAULT_REGION="$REGION"

echo "==> API Gateway"
for id in $(aws apigatewayv2 get-apis --query "Items[?Name=='qroll-http-api'].ApiId" --output text); do
  aws apigatewayv2 delete-api --api-id "$id" && echo "    deleted $id"
done

echo "==> Lambda + logs"
aws lambda delete-function --function-name qroll-api 2>/dev/null && echo "    deleted qroll-api"
aws logs delete-log-group --log-group-name /aws/lambda/qroll-api 2>/dev/null

echo "==> IAM role"
aws iam delete-role-policy --role-name qroll-lambda-role --policy-name qroll-least-privilege 2>/dev/null
aws iam delete-role --role-name qroll-lambda-role 2>/dev/null && echo "    deleted qroll-lambda-role"

echo "==> DynamoDB table"
aws dynamodb delete-table --table-name qroll-attendance >/dev/null 2>&1 && echo "    deleted qroll-attendance"

echo "==> S3 website bucket"
aws s3 rb "s3://$BUCKET" --force >/dev/null 2>&1 && echo "    deleted $BUCKET"

echo "✅ QRoll removed."
