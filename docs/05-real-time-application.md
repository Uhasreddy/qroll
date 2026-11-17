# 5. Real-Time Application: Netflix on AWS — *1 Mark*

## The company
**Netflix** streams films and series to **more than 200 million members in 190+ countries**. Unit V lists Netflix as a notable AWS user.

## The problem
In **2008** a major database corruption in Netflix's own data centre stopped DVD shipments for **3 days**. Netflix saw that a single on-premise data centre could not:
- scale to sudden global demand (new series releases, weekends),
- give high availability across countries, and
- grow quickly enough when it moved from DVDs to streaming.

## The solution: move everything to AWS (2008–2016)
Netflix finished moving all of its streaming infrastructure to AWS in **2016** and closed its last data centre.

```
 User (TV / Mobile)
        │
        ▼
 Amazon Route 53 (DNS) ──► Elastic Load Balancing
                                  │
                                  ▼
                 EC2 Auto Scaling groups (thousands of micro-services)
                     │                 │                 │
                     ▼                 ▼                 ▼
              DynamoDB / Cassandra   Amazon S3        Kinesis / EMR
              (user data, history)  (video masters)  (analytics, recommendations)
                                       │
                                       ▼
                 Encoding on EC2 → Open Connect CDN → User's screen
```

| Netflix need | AWS service | Cloud concept (syllabus) |
|---|---|---|
| Thousands of micro-services | **EC2** + Auto Scaling | IaaS, elasticity (Units II & IV) |
| Store video master files | **Amazon S3** | Object storage, durability |
| Spread traffic | **Elastic Load Balancing** | Load balancing (Unit IV) |
| Survive failures | **Multiple Regions and AZs** | High availability, SLA (Unit I) |
| Personalised recommendations | **EMR, Kinesis, S3 data lake** | Big data analytics |
| Secure access | **IAM** | Cloud security (Unit III) |

## Results
- Streaming hours grew **1,000×** after the migration began.
- Netflix runs **chaos engineering** ("Chaos Monkey"), which randomly stops EC2 instances to prove the system survives failures.
- Netflix adds capacity in minutes for big releases instead of buying servers months ahead.
- Its engineers focus on content and personalisation rather than hardware.

## Other industry examples on AWS
| Industry | Organisation | Use |
|---|---|---|
| Travel | Airbnb, Expedia | Booking platforms, data analytics |
| Education | Coursera | Course video delivery to millions of learners |
| Sports | Formula 1 | Real-time race-car data analysis (F1 Insights) |
| Finance | Coinbase, Intuit | Secure, compliant transaction processing |
| Government / Health | US FDA | Processing drug-safety reports |
| India | Swiggy, Zomato, Ola (popular reported users) | Real-time order and ride matching at scale |

## Link to my demo
My **Demo B** (an EC2 web server behind a security group) is a tiny version of one Netflix micro-service node. Adding an **Auto Scaling group + Load Balancer** in front of many such instances is how Netflix-scale systems are built.
