#!/usr/bin/env bash
# Demo A: host demo/website on Amazon S3 static website hosting.
# Usage: ./deploy-s3-website.sh <globally-unique-bucket-name> [region]
set -euo pipefail

BUCKET="${1:?Usage: $0 <bucket-name> [region]}"
REGION="${2:-ap-south-1}"
HERE="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$HERE/../website"

echo "==> 1. Creating bucket s3://$BUCKET in $REGION"
aws s3 mb "s3://$BUCKET" --region "$REGION"

echo "==> 2. Allowing public bucket policies (turning off Block Public Access)"
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false

echo "==> 3. Enabling static website hosting"
aws s3 website "s3://$BUCKET" --index-document index.html --error-document error.html

echo "==> 4. Attaching public-read bucket policy"
POLICY_FILE="$(mktemp)"
sed "s/BUCKET_NAME/$BUCKET/" "$HERE/bucket-policy.json" > "$POLICY_FILE"
aws s3api put-bucket-policy --bucket "$BUCKET" --policy "file://$POLICY_FILE"
rm -f "$POLICY_FILE"

echo "==> 5. Uploading website files"
aws s3 sync "$SITE_DIR" "s3://$BUCKET" --delete

URL="http://$BUCKET.s3-website.$REGION.amazonaws.com"
echo
echo "✅ Website is live: $URL"
echo "   Try the error page: $URL/does-not-exist"
