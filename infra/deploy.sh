#!/usr/bin/env bash
# Deploy QRoll to AWS: DynamoDB table, IAM role, Lambda function, API Gateway HTTP API, S3 website.
# Usage: ./deploy.sh <globally-unique-bucket-name> [region]
# Safe to re-run: existing resources are reused and the code is updated.
set -euo pipefail

BUCKET="${1:?Usage: $0 <bucket-name> [region]}"
REGION="${2:-ap-southeast-2}"
export AWS_DEFAULT_REGION="$REGION"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$HERE/.."
APP=qroll
TABLE=qroll-attendance
ROLE=qroll-lambda-role
FUNC=qroll-api
SITE_ORIGIN="http://$BUCKET.s3-website-$REGION.amazonaws.com"
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

step() { printf '\n==> %s\n' "$*"; }

# ---------------------------------------------------------------- DynamoDB
step "1. DynamoDB table $TABLE (on-demand, TTL on expiresAt)"
if ! aws dynamodb describe-table --table-name "$TABLE" >/dev/null 2>&1; then
  aws dynamodb create-table --table-name "$TABLE" \
    --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
    --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --tags Key=app,Value=$APP >/dev/null
  aws dynamodb wait table-exists --table-name "$TABLE"
  aws dynamodb update-time-to-live --table-name "$TABLE" \
    --time-to-live-specification Enabled=true,AttributeName=expiresAt >/dev/null
fi
TABLE_ARN=$(aws dynamodb describe-table --table-name "$TABLE" --query Table.TableArn --output text)
echo "    $TABLE_ARN"

# ---------------------------------------------------------------- IAM
step "2. IAM role $ROLE (least privilege: this table + its own logs)"
if ! aws iam get-role --role-name "$ROLE" >/dev/null 2>&1; then
  aws iam create-role --role-name "$ROLE" \
    --assume-role-policy-document "file://$HERE/lambda-trust-policy.json" >/dev/null
  NEW_ROLE=1
fi
sed -e "s|TABLE_ARN|$TABLE_ARN|" -e "s|REGION|$REGION|g" -e "s|ACCOUNT|$ACCOUNT|g" -e "s|FUNC|$FUNC|g" \
  "$HERE/lambda-permissions-policy.json" > "$WORK/policy.json"
aws iam put-role-policy --role-name "$ROLE" --policy-name qroll-least-privilege \
  --policy-document "file://$WORK/policy.json"
ROLE_ARN=$(aws iam get-role --role-name "$ROLE" --query Role.Arn --output text)
[ "${NEW_ROLE:-0}" = 1 ] && { echo "    waiting for IAM role to propagate..."; sleep 12; }

# ---------------------------------------------------------------- Lambda
step "3. Lambda function $FUNC (Python 3.12)"
(cd "$ROOT/backend" && zip -q "$WORK/function.zip" lambda_function.py)
ENV="Variables={TABLE_NAME=$TABLE}"
if aws lambda get-function --function-name "$FUNC" >/dev/null 2>&1; then
  aws lambda update-function-code --function-name "$FUNC" --zip-file "fileb://$WORK/function.zip" >/dev/null
  aws lambda wait function-updated --function-name "$FUNC"
  aws lambda update-function-configuration --function-name "$FUNC" --environment "$ENV" >/dev/null
else
  aws lambda create-function --function-name "$FUNC" --runtime python3.12 \
    --handler lambda_function.lambda_handler --role "$ROLE_ARN" \
    --zip-file "fileb://$WORK/function.zip" --timeout 10 --memory-size 256 \
    --environment "$ENV" --tags app=$APP >/dev/null
fi
aws lambda wait function-active-v2 --function-name "$FUNC"
FUNC_ARN=$(aws lambda get-function --function-name "$FUNC" --query Configuration.FunctionArn --output text)
aws logs put-retention-policy --log-group-name "/aws/lambda/$FUNC" --retention-in-days 7 2>/dev/null || true

# ---------------------------------------------------------------- API Gateway
step "4. API Gateway HTTP API (CORS locked to the website, throttled)"
API_ID=$(aws apigatewayv2 get-apis --query "Items[?Name=='$APP-http-api'].ApiId | [0]" --output text)
if [ "$API_ID" = "None" ] || [ -z "$API_ID" ]; then
  API_ID=$(aws apigatewayv2 create-api --name "$APP-http-api" --protocol-type HTTP \
    --cors-configuration "AllowOrigins=$SITE_ORIGIN,AllowMethods=GET,POST,OPTIONS,AllowHeaders=content-type,x-organizer-pin,MaxAge=600" \
    --tags app=$APP --query ApiId --output text)
  INTEG=$(aws apigatewayv2 create-integration --api-id "$API_ID" --integration-type AWS_PROXY \
    --integration-uri "$FUNC_ARN" --payload-format-version 2.0 --query IntegrationId --output text)
  for R in "POST /events" "GET /events/{id}" "GET /events/{id}/qr" "POST /events/{id}/checkin" \
           "GET /events/{id}/attendees" "POST /events/{id}/close"; do
    aws apigatewayv2 create-route --api-id "$API_ID" --route-key "$R" --target "integrations/$INTEG" >/dev/null
    echo "    route: $R"
  done
  aws apigatewayv2 create-stage --api-id "$API_ID" --stage-name '$default' --auto-deploy \
    --default-route-settings ThrottlingBurstLimit=20,ThrottlingRateLimit=10 >/dev/null
  aws lambda add-permission --function-name "$FUNC" --statement-id apigw-invoke \
    --action lambda:InvokeFunction --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT:$API_ID/*/*" >/dev/null
fi
API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com"
echo "    $API_URL"

# ---------------------------------------------------------------- S3 website
step "5. S3 static website s3://$BUCKET"
if ! aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  aws s3 mb "s3://$BUCKET" >/dev/null
  aws s3api put-bucket-tagging --bucket "$BUCKET" --tagging "TagSet=[{Key=app,Value=$APP}]"
fi
aws s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false
aws s3 website "s3://$BUCKET" --index-document index.html
cat > "$WORK/bucket-policy.json" <<EOF
{"Version":"2012-10-17","Statement":[{"Sid":"PublicReadWebsite","Effect":"Allow","Principal":"*",
 "Action":"s3:GetObject","Resource":"arn:aws:s3:::$BUCKET/*"}]}
EOF
aws s3api put-bucket-policy --bucket "$BUCKET" --policy "file://$WORK/bucket-policy.json"
mkdir -p "$WORK/site" && cp -R "$ROOT/frontend/." "$WORK/site/"
echo "window.QROLL_API = \"$API_URL\";" > "$WORK/site/config.js"
aws s3 sync "$WORK/site" "s3://$BUCKET" --delete --cache-control "no-cache" --only-show-errors

printf '\n✅ QRoll is live\n   Website : %s\n   API     : %s\n' "$SITE_ORIGIN" "$API_URL"
