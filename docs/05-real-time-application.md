# 5. Real-Time Application — *1 mark*

## 5.1 Real-time behaviour in QRoll
QRoll is a **live system**, not a simulation. Every action in the demo reads or writes the real DynamoDB table in AWS:

- A student taps **Check in**. API Gateway → Lambda → DynamoDB transaction completes in about **30–60 ms** on a warm function.
- The organizer dashboard polls every **4 s**, so a new name appears on the projector within a few seconds and the row flashes.
- The QR on the projector **rotates every 30 s**, driven by server time inside Lambda.
- CloudWatch shows each request as it happens (80 invocations, 0 errors during testing).

## 5.2 Industry use case: large-event check-in
**Scenario:** a university tech fest with **3,000 attendees** across 40 workshop sessions on one day.

| Challenge | Traditional approach | QRoll on AWS |
|---|---|---|
| 300 people arrive in 10 minutes for the keynote | Queues at 4 desks with paper lists | Everyone scans the projected QR at once; Lambda scales to parallel requests automatically |
| Peak load for 1 hour, idle the rest of the year | Rent or buy servers sized for the peak | Pay per request; ₹0 when idle |
| Proxy entries for certificates | Hard to detect | Rotating QR + unique register number per session |
| Session-wise reports for certificates | Manual data entry | CSV export per session |
| Data privacy after the fest | Paper sheets left lying around | TTL automatically deletes data after 7 days |

The same serverless pattern (static frontend + API Gateway + Lambda + DynamoDB) is used in industry for:
- **Event ticketing and badge scanning** at conferences.
- **Contact-tracing check-ins** at venues during COVID-19 (QR + serverless backends were widely used).
- **Restaurant QR ordering** and **parking/visitor logs**: short, bursty traffic, ideal for pay-per-request.

## 5.3 Scaling path (how this grows into a production product)
| Need | Add this AWS service |
|---|---|
| HTTPS + custom domain (`attendance.college.edu`) | Amazon CloudFront + AWS Certificate Manager + Route 53 |
| Student login instead of typing a register number | Amazon Cognito (SSO with the college identity provider) |
| Push updates instead of polling | API Gateway WebSocket API or AWS AppSync subscriptions |
| Daily attendance reports emailed to faculty | Amazon EventBridge schedule → Lambda → Amazon SES |
| Analytics (who misses Monday classes?) | DynamoDB export to S3 → Amazon Athena / QuickSight |
| Infrastructure as Code | AWS SAM or CDK instead of shell scripts |
