# Screenshots: live run on 17 Nov 2026 (ap-southeast-2)

| File | Shows |
|---|---|
| `01-create-event.jpg` | Organizer creates the event (title, venue, duration, PIN) |
| `02-live-qr-dashboard.jpg` | Dashboard with the rotating QR and countdown, before any check-ins |
| `03-student-checkin-form.jpg` | Student's phone after scanning the QR |
| `04-student-checked-in.jpg` | Successful check-in confirmation |
| `05-duplicate-blocked.jpg` | Same register number again → blocked (HTTP 409) |
| `06-live-dashboard-attendees.jpg` | Dashboard with 6 live check-ins; QR token already rotated |
| `07-expired-qr-rejected.jpg` | Old QR link used after 2 minutes → rejected (HTTP 403) |
| `08-dynamodb-items.jpg` | DynamoDB table items: one `META` row + one `ATT#<regno>` row per student |
| `09-lambda-function.jpg` | Lambda function `qroll-api` with its API Gateway trigger |
| `10-cloudwatch-metrics.jpg` | CloudWatch: 80 invocations, 0 errors, 100% success |

Sample classmates in the screenshots are demo data entered for testing.
