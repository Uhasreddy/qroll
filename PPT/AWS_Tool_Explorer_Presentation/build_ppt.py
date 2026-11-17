"""Builds AWS_Tool_Explorer.pptx (python-pptx). Run: python3 build_ppt.py"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY = RGBColor(0x23, 0x2F, 0x3E)
NAVY2 = RGBColor(0x2E, 0x3D, 0x50)
ORANGE = RGBColor(0xFF, 0x99, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x16, 0x19, 0x1F)
MUTED = RGBColor(0x5F, 0x6B, 0x7A)
PAPER = RGBColor(0xF4, 0xF6, 0xF8)
LIGHT = RGBColor(0xFF, 0xF4, 0xE0)
REPO = "github.com/yanamalareddy-star/aws-tool-explorer"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height


def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line=None):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1.25)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def text(slide, x, y, w, h, runs, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font="Calibri"):
    """runs: str, or list of paragraphs; each paragraph is str or list of (text, overrides)."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    paras = runs if isinstance(runs, list) else [runs]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(6)
        segs = p if isinstance(p, list) else [(p, {})]
        for seg, o in segs:
            r = para.add_run()
            r.text = seg
            r.font.name = font
            r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", bold)
            r.font.color.rgb = o.get("color", color)
    return tb


def base(title, kicker=None, dark=False):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, W, H, NAVY if dark else PAPER)
    rect(s, 0, 0, Inches(0.18), H, ORANGE)
    if kicker:
        text(s, Inches(0.6), Inches(0.35), Inches(11), Inches(0.4), kicker.upper(), size=13,
             color=ORANGE, bold=True)
    text(s, Inches(0.6), Inches(0.68), Inches(12), Inches(0.9), title, size=32, bold=True,
         color=WHITE if dark else NAVY)
    text(s, Inches(0.6), Inches(7.0), Inches(9), Inches(0.35),
         "21CSE362T Cloud Computing · Tool Explorer: AWS", size=10, color=MUTED)
    text(s, Inches(11.6), Inches(7.0), Inches(1.4), Inches(0.35), str(len(prs.slides)), size=10,
         color=MUTED, align=PP_ALIGN.RIGHT)
    return s


def card(s, x, y, w, h, head, body, head_color=NAVY, fill=WHITE, size=14, accent=ORANGE):
    rect(s, x, y, w, h, fill, MSO_SHAPE.RECTANGLE)
    rect(s, x, y, w, Inches(0.07), accent)
    text(s, x + Inches(0.2), y + Inches(0.18), w - Inches(0.4), Inches(0.5), head, size=18,
         bold=True, color=head_color)
    text(s, x + Inches(0.2), y + Inches(0.7), w - Inches(0.4), h - Inches(0.8), body, size=size,
         color=INK)


def bullets(items):
    return [[("▸  ", {"color": ORANGE, "bold": True}), (t, {})] if isinstance(t, str) else
            [("▸  ", {"color": ORANGE, "bold": True}), (t[0], {"bold": True}), (t[1], {})]
            for t in items]


# 1. Title
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
rect(s, Inches(8.6), 0, Inches(4.733), H, NAVY2)
rect(s, 0, Inches(5.2), Inches(8.6), Inches(0.08), ORANGE)
text(s, Inches(0.8), Inches(1.0), Inches(7.5), Inches(0.5), "TOOL EXPLORER · 21CSE362T CLOUD COMPUTING",
     size=14, color=ORANGE, bold=True)
text(s, Inches(0.8), Inches(1.7), Inches(7.8), Inches(2.4),
     [[("Amazon Web Services", {})], [("(AWS)", {"color": ORANGE})]], size=54, bold=True, color=WHITE)
text(s, Inches(0.8), Inches(4.0), Inches(7.6), Inches(1.0),
     "Exploring the world's leading cloud platform: services, a hands-on demo, features and a real-world use case",
     size=18, color=RGBColor(0xC9, 0xD1, 0xD9))
text(s, Inches(0.8), Inches(5.5), Inches(7.6), Inches(1.2),
     [[("Presented by: ", {"color": ORANGE, "bold": True}), ("Yanamala Uhas Reddy  ·  RA2311003010363", {})],
      [("Repository: ", {"color": ORANGE, "bold": True}), (REPO, {})]], size=15, color=WHITE)
for i, (big, small) in enumerate([("2006", "Launched"), ("200+", "Services"), ("~1/3", "Cloud market share")]):
    y = Inches(1.3 + i * 1.75)
    text(s, Inches(9.1), y, Inches(3.8), Inches(0.9), big, size=46, bold=True, color=ORANGE)
    text(s, Inches(9.1), y + Inches(0.85), Inches(3.8), Inches(0.5), small, size=16, color=WHITE)

# 2. Agenda
s = base("Agenda", "What this presentation covers")
agenda = [("1", "Tool Introduction", "1 mark"), ("2", "Service Exploration: IaaS · PaaS · SaaS", "2 marks"),
          ("3", "Practical Demonstration: S3 website + EC2 server", "2 marks"),
          ("4", "Feature Identification: features, benefits, applications", "2 marks"),
          ("5", "Real-Time Application: Netflix on AWS", "1 mark"), ("6", "Viva Quick Facts", "2 marks")]
for i, (n, t, m) in enumerate(agenda):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.2), Inches(1.9 + row * 1.6)
    rect(s, x, y, Inches(5.9), Inches(1.3), WHITE)
    rect(s, x, y, Inches(1.1), Inches(1.3), NAVY)
    text(s, x, y, Inches(1.1), Inches(1.3), n, size=36, bold=True, color=ORANGE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(1.3), y + Inches(0.15), Inches(4.5), Inches(0.7), t, size=18, bold=True, color=NAVY)
    text(s, x + Inches(1.3), y + Inches(0.8), Inches(4.5), Inches(0.4), m, size=13, color=MUTED)

# 3. Introduction
s = base("What is AWS?", "1 · Tool Introduction")
text(s, Inches(0.6), Inches(1.7), Inches(7.2), Inches(5), bullets([
    ("Amazon Web Services ", "is Amazon's public cloud platform, launched in 2006 with S3 and EC2."),
    ("200+ services ", "for compute, storage, networking, databases, analytics, AI/ML and IoT."),
    ("On-demand, pay-as-you-go: ", "rent servers and software over the Internet, pay only for what you use."),
    ("Purpose: ", "replace on-premise data centres and turn CapEx into OpEx (better TCO)."),
    ("Access: ", "Management Console (GUI), AWS CLI, SDKs (boto3) and CloudFormation."),
]), size=18)
card(s, Inches(8.2), Inches(1.7), Inches(4.5), Inches(4.9), "Why it matters", bullets([
    "Market leader: about one-third of the cloud market",
    "Pioneered IaaS; others followed its model",
    "Shows all 5 NIST characteristics",
    "Offers IaaS, PaaS and SaaS",
    "SLAs: EC2 99.99% · S3 11-nines durability",
    "Used by Netflix, Airbnb, Coursera, F1, FDA",
]), size=15)

# 4. Global infrastructure
s = base("AWS Global Infrastructure", "1 · Tool Introduction")
for i, (h, b) in enumerate([
        ("Regions", "Separate geographic areas, e.g. ap-south-1 (Mumbai), us-east-1 (N. Virginia). Choose for latency, cost and data-residency laws."),
        ("Availability Zones", "One or more isolated data centres in each Region, linked by low-latency fibre. Deploying across AZs gives fault tolerance."),
        ("Edge Locations", "400+ points of presence used by CloudFront (CDN) and Route 53 to serve content close to users.")]):
    card(s, Inches(0.6 + i * 4.15), Inches(1.8), Inches(3.9), Inches(3.2), h, b, size=16)
rect(s, Inches(0.6), Inches(5.35), Inches(12.1), Inches(1.3), NAVY)
text(s, Inches(0.9), Inches(5.35), Inches(11.6), Inches(1.3),
     [[("200+ data centres ", {"color": ORANGE, "bold": True}),
       ("worldwide, the most of the three hyperscalers, with major hubs in Northern Virginia, Oregon and Frankfurt (Unit V).", {})]],
     size=18, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)

# 5. Service models stack
s = base("Cloud Service Models on AWS", "2 · Service Exploration")
layers = [("SaaS", "Ready-to-use software", "Amazon WorkMail · Chime · QuickSight · Connect", Inches(7.2)),
          ("PaaS", "Platform: runtime, OS, DB managed", "Elastic Beanstalk · Amazon RDS · AWS Lambda", Inches(9.2)),
          ("IaaS", "Virtual servers, storage, network", "Amazon EC2 · Amazon S3 · EBS · VPC", Inches(11.2))]
for i, (n, d, ex, w) in enumerate(layers):
    y = Inches(1.8 + i * 1.45)
    x = (W - w) / 2 + Inches(0.1)
    rect(s, x, y, w, Inches(1.25), [ORANGE, NAVY2, NAVY][i])
    col = NAVY if i == 0 else WHITE
    text(s, x + Inches(0.3), y, Inches(1.6), Inches(1.25), n, size=30, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(2.0), y + Inches(0.12), w - Inches(2.2), Inches(1.1),
         [[(d, {"bold": True})], [(ex, {})]], size=16, color=col)
text(s, Inches(0.6), Inches(6.25), Inches(12.1), Inches(0.6),
     [[("Moving up the stack, ", {}), ("AWS manages more ", {"bold": True, "color": NAVY}),
       ("and you manage less. IaaS: you manage OS + app. PaaS: only code + data. SaaS: just use it.", {})]],
     size=16, color=INK, align=PP_ALIGN.CENTER)

# 6. IaaS
s = base("IaaS: Infrastructure as a Service", "2 · Service Exploration")
card(s, Inches(0.6), Inches(1.7), Inches(6.0), Inches(4.9), "Amazon EC2 (Elastic Compute Cloud)", bullets([
    "Resizable virtual machines on the Nitro hypervisor (Unit IV)",
    "Launched from an AMI: OS + software template (VM imaging)",
    "Families: general (t3, m7), compute (c7), memory (r7), GPU (p5)",
    "Pricing: On-Demand, Reserved, Savings Plans, Spot (up to 90% off)",
    ("Example: ", "exam portal on 2 × t3.medium during results week"),
]), size=15)
card(s, Inches(6.9), Inches(1.7), Inches(5.8), Inches(4.9), "Amazon S3 · EBS · VPC", bullets([
    ("S3: ", "object storage in buckets, unlimited capacity, 11-nines durability"),
    "Storage classes: Standard, Intelligent-Tiering, IA, Glacier",
    ("EBS: ", "block-storage disks attached to EC2"),
    ("VPC: ", "your own isolated virtual network with subnets and gateways"),
    ("Example: ", "lecture videos, backups, static website (our demo)"),
]), size=15)

# 7. PaaS & SaaS
s = base("PaaS and SaaS", "2 · Service Exploration")
items = [("Elastic Beanstalk", "PaaS", "Upload code; AWS creates EC2, load balancer and Auto Scaling.\nEx: deploy a Flask app from a .zip"),
         ("Amazon RDS", "PaaS", "Managed MySQL / PostgreSQL / Aurora with backups, patching and Multi-AZ.\nEx: university ERP database"),
         ("AWS Lambda", "PaaS / FaaS", "Serverless: code runs only when triggered, billed per ms.\nEx: thumbnail on S3 upload"),
         ("Amazon WorkMail", "SaaS", "Managed business e-mail and calendar.\nEx: company mail without a mail server"),
         ("Amazon Chime", "SaaS", "Online meetings, video calls and chat.\nEx: team meetings, webinars"),
         ("Amazon QuickSight", "SaaS", "Business-intelligence dashboards.\nEx: sales dashboard for managers")]
for i, (h, tag, b) in enumerate(items):
    col, row = i % 3, i // 3
    x, y = Inches(0.6 + col * 4.1), Inches(1.7 + row * 2.55)
    card(s, x, y, Inches(3.85), Inches(2.35), h, b, size=13, accent=ORANGE if tag == "SaaS" else NAVY)
    text(s, x + Inches(2.4), y + Inches(0.2), Inches(1.3), Inches(0.4), tag, size=11, bold=True, color=MUTED,
         align=PP_ALIGN.RIGHT)

# 8. Comparison
s = base("AWS vs Microsoft Azure vs Google Cloud", "2 · Service Exploration (Unit V)")
rows = [("Need", "AWS", "Azure", "Google Cloud"), ("Virtual machines", "EC2", "Virtual Machines", "Compute Engine"),
        ("Serverless", "Lambda", "Azure Functions", "Cloud Functions"), ("Object storage", "S3", "Blob Storage", "Cloud Storage"),
        ("PaaS app hosting", "Elastic Beanstalk", "App Service", "App Engine"), ("Launched", "2006", "2010", "2011"),
        ("Known for", "Widest service range", "Microsoft / Windows integration", "DevOps, data & AI")]
tbl = s.shapes.add_table(len(rows), 4, Inches(0.6), Inches(1.8), Inches(12.1), Inches(4.6)).table
for r, row in enumerate(rows):
    for c, val in enumerate(row):
        cell = tbl.cell(r, c)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r == 0 else (LIGHT if c == 1 else WHITE)
        p = cell.text_frame.paragraphs[0]
        p.runs[0].font.size = Pt(17)
        p.runs[0].font.bold = r == 0 or c == 0
        p.runs[0].font.color.rgb = (ORANGE if c == 1 else WHITE) if r == 0 else INK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

# 9. Demo A
s = base("Demo A: Static Website on Amazon S3", "3 · Practical Demonstration")
steps = ["Create bucket (unique name, region ap-southeast-2)", "Untick Block all public access",
         "Upload index.html, error.html, style.css", "Properties → Static website hosting → Enable",
         "Permissions → Bucket policy (public s3:GetObject)", "Open the bucket website endpoint ✅"]
for i, st in enumerate(steps):
    y = Inches(1.75 + i * 0.82)
    rect(s, Inches(0.6), y, Inches(0.62), Inches(0.62), ORANGE, MSO_SHAPE.OVAL)
    text(s, Inches(0.6), y, Inches(0.62), Inches(0.62), str(i + 1), size=18, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(1.4), y, Inches(5.6), Inches(0.62), st, size=17, color=INK, anchor=MSO_ANCHOR.MIDDLE)
rect(s, Inches(7.3), Inches(1.75), Inches(5.4), Inches(4.75), NAVY)
text(s, Inches(7.55), Inches(1.9), Inches(5.0), Inches(4.5),
     [[("# CLI equivalent", {"color": ORANGE})],
      "aws s3 mb s3://tool-explorer-ra2311003010363",
      "aws s3api put-public-access-block ...",
      "aws s3 website s3://tool-explorer-ra2311003010363 \\",
      "   --index-document index.html \\",
      "   --error-document error.html",
      "aws s3api put-bucket-policy ...",
      "aws s3 sync ../website s3://tool-explorer-ra2311003010363",
      [("", {})],
      [("→ http://tool-explorer-ra2311003010363.s3-website", {"color": ORANGE})],
      [("   .ap-southeast-2.amazonaws.com", {"color": ORANGE})]],
     size=13, color=WHITE, font="Consolas")

# 10. Demo B
s = base("Demo B: Web Server on Amazon EC2", "3 · Practical Demonstration")
steps = ["Launch instance: name tool-explorer-web", "AMI: Amazon Linux 2023 · type t3.micro (Free Tier)",
         "Create key pair (.pem) for SSH", "Security group: allow SSH 22 (my IP) and HTTP 80 (anywhere)",
         "User data: script installs Apache and writes the page", "Running, 2/2 checks → open http://<public-ip> ✅"]
for i, st in enumerate(steps):
    y = Inches(1.75 + i * 0.82)
    rect(s, Inches(0.6), y, Inches(0.62), Inches(0.62), ORANGE, MSO_SHAPE.OVAL)
    text(s, Inches(0.6), y, Inches(0.62), Inches(0.62), str(i + 1), size=18, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(1.4), y, Inches(5.7), Inches(0.62), st, size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)
rect(s, Inches(7.3), Inches(1.75), Inches(5.4), Inches(2.6), NAVY)
text(s, Inches(7.55), Inches(1.88), Inches(5.0), Inches(2.4),
     [[("# ec2-user-data.sh (runs on first boot)", {"color": ORANGE})],
      "#!/bin/bash", "dnf install -y httpd", "systemctl enable --now httpd",
      "# read instance-id + AZ from metadata", "cat > /var/www/html/index.html ..."],
     size=13, color=WHITE, font="Consolas")
card(s, Inches(7.3), Inches(4.55), Inches(5.4), Inches(1.95), "Concepts shown", bullets([
    "Virtualization (VM from an AMI)", "Security group as a firewall (Unit III)", "Monitoring in CloudWatch · Terminate after the demo",
]), size=13)

# 10b. Real results
SHOTS = Path(__file__).resolve().parents[2] / "screenshots"
s = base("Demo Results: Live on AWS", "3 · Practical Demonstration (actual run, ap-southeast-2)")
shots = [("01-s3-bucket-objects.jpg", "S3 bucket with uploaded files"), ("03-s3-site-live.jpg", "Website live from S3 endpoint"),
         ("05-ec2-instance-running.jpg", "EC2 t3.micro instance running"), ("07-ec2-site-live.jpg", "Apache page served by EC2")]
for i, (f, cap) in enumerate(shots):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.15), Inches(1.55 + row * 2.75)
    pic = s.shapes.add_picture(str(SHOTS / f), x, y, height=Inches(2.25))
    if pic.width > Inches(5.95):
        pic.width, pic.height = Inches(5.95), int(pic.height * Inches(5.95) / pic.width)
    text(s, x, y + Inches(2.28), Inches(5.95), Inches(0.35), cap, size=13, bold=True, color=NAVY)

# 11. Features
s = base("Key Features of AWS", "4 · Feature Identification")
feats = [("Elasticity & Auto Scaling", "Add or remove capacity automatically"), ("Pay-as-you-go", "Per-second billing; Spot up to 90% off"),
         ("Global infrastructure", "Regions, AZs, Edge Locations"), ("High availability", "Multi-AZ; S3 11-nines durability"),
         ("Load balancing", "ELB spreads traffic (Unit IV)"), ("Virtualization", "Nitro hypervisor, AMIs"),
         ("Security & IAM", "Roles, policies, MFA, KMS encryption"), ("Monitoring", "CloudWatch metrics, CloudTrail audit"),
         ("Serverless", "Lambda, API Gateway, DynamoDB"), ("Infrastructure as Code", "CloudFormation, CDK")]
for i, (h, b) in enumerate(feats):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.15), Inches(1.65 + row * 1.03)
    rect(s, x, y, Inches(5.95), Inches(0.9), WHITE)
    rect(s, x, y, Inches(0.09), Inches(0.9), ORANGE)
    text(s, x + Inches(0.3), y, Inches(5.5), Inches(0.9),
         [[(h + "  ", {"bold": True, "color": NAVY}), ("·  " + b, {"color": MUTED})]], size=16,
         anchor=MSO_ANCHOR.MIDDLE)

# 12. Benefits & applications
s = base("Benefits and Applications", "4 · Feature Identification")
card(s, Inches(0.6), Inches(1.7), Inches(5.6), Inches(4.95), "Benefits", bullets([
    "Lower cost and better TCO: no CapEx (Unit I)", "Speed: resources in minutes, not weeks",
    "Scales for spikes (sales, results day)", "Reliability: multi-AZ, published SLAs",
    "Compliance: ISO 27001, SOC, PCI-DSS, HIPAA", "Free Tier for students to learn",
]), size=15)
apps = [("Web & mobile", "EC2, S3, Amplify"), ("Media streaming", "S3, CloudFront"), ("E-commerce", "Auto Scaling, RDS"),
        ("Big data", "EMR, Athena, Redshift"), ("AI / ML", "SageMaker, Bedrock"), ("Backup & DR", "S3 Glacier, AWS Backup"),
        ("IoT", "IoT Core, Kinesis"), ("Education", "Coursera on EC2 + S3")]
text(s, Inches(6.6), Inches(1.75), Inches(6), Inches(0.5), "Applications", size=18, bold=True, color=NAVY)
for i, (h, b) in enumerate(apps):
    col, row = i % 2, i // 2
    x, y = Inches(6.6 + col * 3.05), Inches(2.35 + row * 1.08)
    rect(s, x, y, Inches(2.9), Inches(0.95), NAVY)
    text(s, x + Inches(0.15), y + Inches(0.05), Inches(2.6), Inches(0.9),
         [[(h, {"bold": True, "color": ORANGE})], [(b, {"size": 12})]], size=15, color=WHITE)

# 13. Netflix
s = base("Real-Time Application: Netflix on AWS", "5 · Real-Time Application")
text(s, Inches(0.6), Inches(1.65), Inches(5.6), Inches(5), [
    [("Problem (2008): ", {"bold": True, "color": NAVY}), ("database corruption in its own data centre stopped shipments for 3 days.", {})],
    [("Solution: ", {"bold": True, "color": NAVY}), ("moved everything to AWS. The last data centre closed in 2016.", {})],
    [("Scale: ", {"bold": True, "color": NAVY}), ("200M+ members in 190+ countries; streaming hours grew 1000×.", {})],
    [("Chaos Monkey: ", {"bold": True, "color": NAVY}), ("randomly kills EC2 instances to prove the system survives failure.", {})],
], size=17)
flow = [("Route 53 + ELB", "DNS & load balancing"), ("EC2 Auto Scaling", "Thousands of micro-services"),
        ("S3 · DynamoDB", "Video masters, user data"), ("EMR · Kinesis", "Analytics & recommendations"),
        ("Multi-Region / AZ", "High availability")]
for i, (h, b) in enumerate(flow):
    y = Inches(1.65 + i * 1.0)
    rect(s, Inches(6.8), y, Inches(5.9), Inches(0.82), NAVY if i % 2 == 0 else NAVY2)
    text(s, Inches(7.05), y, Inches(5.5), Inches(0.82),
         [[(h, {"bold": True, "color": ORANGE}), ("   " + b, {})]], size=16, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    if i < 4:
        text(s, Inches(9.55), y + Inches(0.72), Inches(0.4), Inches(0.3), "▼", size=11, color=ORANGE, align=PP_ALIGN.CENTER)

# 14. Syllabus mapping
s = base("Linking AWS to Our Syllabus", "Concept mapping")
rows = [("Unit", "Topic", "Seen in AWS"), ("I", "Cloud types, benefits, TCO, SLA", "Public cloud, pay-as-you-go, EC2 99.99% SLA"),
        ("II", "Cloud stack, IaaS / PaaS / SaaS", "EC2 & S3 · Beanstalk & RDS · WorkMail"),
        ("III", "Cloud security, identity", "IAM, security groups, shared responsibility"),
        ("IV", "Virtualization, hypervisors, load balancing", "Nitro hypervisor, AMIs, Elastic Load Balancing"),
        ("V", "Amazon, Microsoft, Google", "AWS platform vs Azure vs GCP, case studies")]
tbl = s.shapes.add_table(len(rows), 3, Inches(0.6), Inches(1.8), Inches(12.1), Inches(4.4)).table
tbl.columns[0].width, tbl.columns[1].width, tbl.columns[2].width = Inches(1.2), Inches(5.0), Inches(5.9)
for r, row in enumerate(rows):
    for c, val in enumerate(row):
        cell = tbl.cell(r, c)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r == 0 else WHITE
        run = cell.text_frame.paragraphs[0].runs[0]
        run.font.size = Pt(17)
        run.font.bold = r == 0 or c == 0
        run.font.color.rgb = WHITE if r == 0 else (ORANGE if c == 0 else INK)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

# 15. Viva quick facts
s = base("Viva: Quick Facts", "6 · Viva")
qa = [("EC2 vs Lambda?", "VM you manage vs serverless function billed per request"),
      ("S3 vs EBS?", "Object storage over HTTP vs block disk for one EC2"),
      ("What is an AMI?", "Template (OS + software) used to launch EC2"),
      ("Shared responsibility?", "AWS: security OF the cloud · You: security IN it"),
      ("Security group?", "Stateful virtual firewall for an instance"),
      ("User data?", "Script that runs on first boot (installed Apache)"),
      ("Stop vs Terminate?", "Stop keeps the disk; Terminate deletes it"),
      ("Avoid charges?", "Terminate EC2, delete bucket, set a Budget alert")]
for i, (q, a) in enumerate(qa):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.15), Inches(1.65 + row * 1.27)
    rect(s, x, y, Inches(5.95), Inches(1.12), WHITE)
    text(s, x + Inches(0.2), y + Inches(0.08), Inches(5.6), Inches(1.0),
         [[("Q. " + q, {"bold": True, "color": NAVY})], [(a, {"color": INK})]], size=15)

# 16. Conclusion
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
rect(s, 0, 0, Inches(0.18), H, ORANGE)
text(s, Inches(0.8), Inches(0.9), Inches(11), Inches(0.5), "CONCLUSION", size=14, bold=True, color=ORANGE)
text(s, Inches(0.8), Inches(1.5), Inches(11.5), Inches(3.2), bullets([
    "AWS is the most widely used cloud platform, covering IaaS, PaaS and SaaS.",
    "In the demo, a website went live on S3 and on an EC2 VM within minutes, with no hardware bought.",
    "Its key strengths are elasticity, pay-as-you-go pricing, global reach and strong security.",
    "Netflix shows AWS working at global scale.",
]), size=20, color=WHITE)
text(s, Inches(0.8), Inches(4.9), Inches(11.5), Inches(1.0), "Thank you! Questions?", size=44, bold=True, color=WHITE)
text(s, Inches(0.8), Inches(6.0), Inches(11.5), Inches(0.5),
     [[("Code, docs & this deck: ", {"color": ORANGE, "bold": True}), (REPO, {})]], size=16, color=WHITE)

cp = prs.core_properties
cp.author = cp.last_modified_by = "Yanamala Uhas Reddy"
cp.title = "Tool Explorer: Amazon Web Services (AWS)"
cp.subject = "21CSE362T Cloud Computing"

out = Path(__file__).with_name("AWS_Tool_Explorer.pptx")
prs.save(out)
print("saved", out, len(prs.slides), "slides")
