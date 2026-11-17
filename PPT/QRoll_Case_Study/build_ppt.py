"""Builds QRoll_Case_Study.pptx with python-pptx. Run: python3 build_ppt.py"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

INK = RGBColor(0x0F, 0x17, 0x2A)
INK2 = RGBColor(0x1E, 0x29, 0x3B)
SLATE = RGBColor(0x33, 0x41, 0x55)
MUTED = RGBColor(0x64, 0x74, 0x8B)
LINE = RGBColor(0xE2, 0xE8, 0xF0)
PAPER = RGBColor(0xF8, 0xFA, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEAL = RGBColor(0x0D, 0x94, 0x88)
TEAL_SOFT = RGBColor(0xCC, 0xFB, 0xF1)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
AMBER_SOFT = RGBColor(0xFE, 0xF3, 0xC7)
RED = RGBColor(0xB9, 0x1C, 0x1C)
RED_SOFT = RGBColor(0xFE, 0xE2, 0xE2)
GREEN = RGBColor(0x15, 0x80, 0x3D)

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "screenshots"
SITE = "qroll-ra2311003010363.s3-website-ap-southeast-2.amazonaws.com"
REPO = "github.com/Uhasreddy/qroll"
FONT = "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
TOTAL = 16


def box(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, lw=1.0):
    sh = s.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = 0.08
    return sh


def txt(s, x, y, w, h, paras, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font=FONT, spacing=4):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    paras = paras if isinstance(paras, list) else [paras]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(spacing)
        runs = p if isinstance(p, list) else [(p, {})]
        for t, o in runs:
            r = para.add_run()
            r.text = t
            r.font.name = o.get("font", font)
            r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", bold)
            r.font.color.rgb = o.get("color", color)
    return tb


def arrow(s, x1, y1, x2, y2, color=SLATE, width=1.75, dashed=False):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb = color
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    if dashed:
        prst = etree.SubElement(ln, qn("a:prstDash"))
        prst.set("val", "dash")
    tail = etree.SubElement(ln, qn("a:tailEnd"))
    tail.set("type", "triangle")
    tail.set("w", "med")
    tail.set("len", "med")
    return c


def frame(title, kicker, dark=False):
    s = prs.slides.add_slide(BLANK)
    box(s, 0, 0, W, H, INK if dark else PAPER)
    n = len(prs.slides)
    txt(s, Inches(0.6), Inches(0.38), Inches(9), Inches(0.35),
        [[(f"{n:02d}  ", {"color": TEAL, "bold": True}), (kicker.upper(), {"color": MUTED if not dark else RGBColor(0x94, 0xA3, 0xB8)})]],
        size=12, bold=True)
    txt(s, Inches(0.6), Inches(0.7), Inches(12.1), Inches(0.8), title, size=30, bold=True,
        color=WHITE if dark else INK)
    box(s, Inches(0.6), Inches(1.42), Inches(0.9), Inches(0.06), TEAL)
    txt(s, Inches(0.6), Inches(7.02), Inches(8), Inches(0.3), "QRoll  ·  Serverless QR attendance on AWS",
        size=10, color=MUTED)
    txt(s, Inches(11.7), Inches(7.02), Inches(1.0), Inches(0.3), f"{n} / {TOTAL}", size=10, color=MUTED,
        align=PP_ALIGN.RIGHT)
    return s


def card(s, x, y, w, h, head, body, accent=TEAL, size=13, fill=WHITE, head_color=INK):
    box(s, x, y, w, h, fill, LINE, MSO_SHAPE.ROUNDED_RECTANGLE)
    box(s, x + Inches(0.2), y + Inches(0.22), Inches(0.38), Inches(0.06), accent)
    txt(s, x + Inches(0.2), y + Inches(0.34), w - Inches(0.4), Inches(0.5), head, size=16, bold=True, color=head_color)
    txt(s, x + Inches(0.2), y + Inches(0.84), w - Inches(0.4), h - Inches(0.95), body, size=size, color=SLATE)


def chip(s, x, y, label, fill=TEAL_SOFT, color=TEAL, w=None, size=11):
    w = w or Inches(0.13 * len(label) + 0.35)
    b = box(s, x, y, w, Inches(0.34), fill, None, MSO_SHAPE.ROUNDED_RECTANGLE)
    b.adjustments[0] = 0.5
    txt(s, x, y, w, Inches(0.34), label, size=size, bold=True, color=color, align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE)
    return w


def pic(s, name, x, y, w=None, h=None, border=True):
    p = s.shapes.add_picture(str(SHOTS / name), x, y, width=w, height=h)
    if border:
        p.line.color.rgb = LINE
        p.line.width = Pt(1)
    return p


def table(s, x, y, w, rows, col_w, size=13, head_fill=INK, row_h=0.42, first_bold=True):
    t = s.shapes.add_table(len(rows), len(rows[0]), x, y, w, Inches(row_h * len(rows))).table
    for i, cw in enumerate(col_w):
        t.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        t.rows[r].height = Inches(row_h)
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = head_fill if r == 0 else (WHITE if r % 2 else PAPER)
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.name = FONT
                    run.font.size = Pt(size if r else size - 1)
                    run.font.bold = r == 0 or (c == 0 and first_bold)
                    run.font.color.rgb = WHITE if r == 0 else (INK if c == 0 else SLATE)
    return t


# ============================================================ 1. Title
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, W, H, INK)
box(s, Inches(8.25), 0, Inches(5.083), H, INK2)
txt(s, Inches(0.7), Inches(0.75), Inches(7.4), Inches(0.4), "CLOUD COMPUTING  ·  21CSE362T  ·  CASE STUDY", size=13,
    bold=True, color=TEAL)
logo = box(s, Inches(0.7), Inches(1.5), Inches(1.05), Inches(1.05), TEAL, None, MSO_SHAPE.ROUNDED_RECTANGLE)
logo.adjustments[0] = 0.18
txt(s, Inches(0.7), Inches(1.5), Inches(1.05), Inches(1.05), "QR", size=34, bold=True, color=WHITE,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.95), Inches(1.4), Inches(6), Inches(1.2), "QRoll", size=66, bold=True, color=WHITE)
txt(s, Inches(0.7), Inches(2.85), Inches(7.4), Inches(1.4),
    [[("Serverless QR attendance that ", {}), ("stops proxies", {"color": TEAL})],
     [("and costs almost nothing to run.", {})]], size=26, bold=True, color=WHITE)
x = Inches(0.7)
for lab in ["AWS Lambda", "API Gateway", "DynamoDB", "Amazon S3"]:
    x += chip(s, x, Inches(4.45), lab, fill=RGBColor(0x13, 0x4E, 0x4A), color=TEAL_SOFT, size=12) + Inches(0.12)
txt(s, Inches(0.7), Inches(5.55), Inches(7.4), Inches(1.0),
    [[("Yanamala Uhas Reddy", {"bold": True, "color": WHITE})],
     [("RA2311003010363  ·  B.Tech CSE", {"color": RGBColor(0x94, 0xA3, 0xB8)})]], size=17)
# phone mock with real screenshot
box(s, Inches(9.35), Inches(0.75), Inches(2.95), Inches(6.0), RGBColor(0x0B, 0x11, 0x20), RGBColor(0x47, 0x55, 0x69),
    MSO_SHAPE.ROUNDED_RECTANGLE, lw=2).adjustments[0] = 0.12
pic(s, "04-student-checked-in.jpg", Inches(9.53), Inches(1.0), w=Inches(2.6), border=False)
txt(s, Inches(8.6), Inches(6.85), Inches(4.5), Inches(0.35), "Real screenshot from the live deployment", size=11,
    color=RGBColor(0x94, 0xA3, 0xB8), align=PP_ALIGN.CENTER)

# ============================================================ 2. The case
s = frame("The case: attendance is slow and easy to fake", "Case brief")
cols = [
    ("PROBLEM", RED, RED_SOFT, "Paper sheets waste 5–10 minutes of each lecture. Friends sign for absentees (\"proxy\"), and someone has to type the sheet into Excel. A Google Form link can simply be forwarded."),
    ("INTERVENTION", TEAL, TEAL_SOFT, "QRoll: the organizer projects a QR that changes every 30 s. Students scan, type name + register number, and appear live on the dashboard. Fully serverless on AWS."),
    ("CLOUD EVIDENCE", AMBER, AMBER_SOFT, "Deployed live in ap-southeast-2. 10/10 end-to-end API tests pass. CloudWatch: 80 invocations, 0 errors. Duplicates → 409, expired QR → 403, late → 410."),
]
for i, (h, c, soft, b) in enumerate(cols):
    x = Inches(0.6 + i * 4.1)
    box(s, x, Inches(1.85), Inches(3.85), Inches(3.05), WHITE, LINE, MSO_SHAPE.ROUNDED_RECTANGLE)
    chip(s, x + Inches(0.25), Inches(2.1), h, fill=soft, color=c, size=11)
    txt(s, x + Inches(0.25), Inches(2.62), Inches(3.4), Inches(2.2), b, size=14, color=SLATE)
box(s, Inches(0.6), Inches(5.2), Inches(12.1), Inches(1.5), INK, None, MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, Inches(0.95), Inches(5.32), Inches(11.4), Inches(0.35), "CASE QUESTION", size=12, bold=True, color=TEAL)
txt(s, Inches(0.95), Inches(5.68), Inches(11.4), Inches(0.9),
    "Can a fully serverless app take attendance faster than paper, block forwarded-link proxies and duplicates, and run for almost ₹0?",
    size=20, bold=True, color=WHITE)

# ============================================================ 3. Tool introduction
s = frame("Tool introduction: AWS serverless", "Tool introduction · 1 mark")
txt(s, Inches(0.6), Inches(1.75), Inches(5.0), Inches(4.8), [
    [("Amazon Web Services", {"bold": True, "color": INK}), (" is Amazon's public cloud (since 2006), with 200+ pay-as-you-go services and the largest market share (Unit V).", {})],
    [("Serverless", {"bold": True, "color": INK}), (" means AWS runs, patches and scales the servers. We supply only code and data, and pay only when a request arrives.", {})],
    [("Cloud characteristics shown (Unit I): ", {"bold": True, "color": INK}),
     ("on-demand self-service, rapid elasticity, measured service, resource pooling.", {})],
], size=15, color=SLATE, spacing=12)
rows = [["AWS service", "What it is", "Role in QRoll"],
        ["AWS Lambda", "Run code on demand (FaaS)", "Whole backend: 6 routes, Python 3.12"],
        ["API Gateway", "Managed HTTPS API front door", "Routing, CORS, throttling 10 rps"],
        ["DynamoDB", "Managed NoSQL database", "Events + check-ins, transactions, TTL"],
        ["Amazon S3", "Object storage + static hosting", "Serves the 3 web pages"],
        ["IAM", "Identity & access control", "Lambda may touch 1 table only"],
        ["CloudWatch", "Logs & metrics", "Invocations, duration, errors"]]
table(s, Inches(5.9), Inches(1.8), Inches(6.8), rows, [1.6, 2.5, 2.7], size=13, row_h=0.6)

# ============================================================ 4. Service models
s = frame("Service model mapping: the job each service actually does", "Service exploration · 2 marks")
models = [
    ("IaaS", "Not used", "No EC2 / VM anywhere. Not renting servers is the main design decision: no OS patching, no idle cost.", RED, RED_SOFT),
    ("FaaS / PaaS", "AWS Lambda · API Gateway", "We upload a function and declare routes; AWS provides runtime, scaling and HTTPS.", TEAL, TEAL_SOFT),
    ("DBaaS", "Amazon DynamoDB", "No DB server or capacity planning. On-demand mode, replicated across 3 AZs.", TEAL, TEAL_SOFT),
    ("SaaS", "Console · CloudWatch · GitHub", "Finished software we only use: manage resources, read metrics, host code.", AMBER, AMBER_SOFT),
]
for i, (m, svc, why, c, soft) in enumerate(models):
    y = Inches(1.75 + i * 1.0)
    box(s, Inches(0.6), y, Inches(7.3), Inches(0.88), WHITE, LINE, MSO_SHAPE.ROUNDED_RECTANGLE)
    chip(s, Inches(0.8), y + Inches(0.27), m, fill=soft, color=c, w=Inches(1.45), size=12)
    txt(s, Inches(2.4), y + Inches(0.08), Inches(5.4), Inches(0.35), svc, size=14, bold=True, color=INK)
    txt(s, Inches(2.4), y + Inches(0.42), Inches(5.4), Inches(0.45), why, size=11.5, color=SLATE)
txt(s, Inches(0.6), Inches(5.85), Inches(7.3), Inches(0.9),
    [[("QRoll itself behaves like a SaaS product: ", {"bold": True, "color": INK}),
      ("an organizer opens a URL and uses it with nothing to install. It is built on FaaS/PaaS, not IaaS.", {})]],
    size=13, color=SLATE)
rows = [["Layer", "EC2 (IaaS)", "QRoll"],
        ["Hardware, network", "AWS", "AWS"],
        ["OS patches", "Us", "AWS"],
        ["Runtime", "Us", "AWS"],
        ["Scaling / LB", "Us", "AWS"],
        ["Database server", "Us", "AWS"],
        ["Code + data + IAM", "Us", "Us"]]
txt(s, Inches(8.3), Inches(1.72), Inches(4.4), Inches(0.4), "Who manages what (Unit III)", size=14, bold=True, color=INK)
t = table(s, Inches(8.3), Inches(2.15), Inches(4.4), rows, [1.9, 1.25, 1.25], size=13, row_h=0.52)
for r in range(1, 6):
    cell = t.cell(r, 2)
    cell.fill.fore_color.rgb = TEAL_SOFT
    cell.text_frame.paragraphs[0].runs[0].font.color.rgb = TEAL
    cell.text_frame.paragraphs[0].runs[0].font.bold = True

# ============================================================ 5. Architecture
s = frame("System architecture", "Solution design")
def node(x, y, w, h, title, sub, fill=WHITE, line=LINE, tc=INK, sc=SLATE):
    box(s, x, y, w, h, fill, line, MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.25)
    txt(s, x, y + Inches(0.1), w, Inches(0.4), title, size=15, bold=True, color=tc, align=PP_ALIGN.CENTER)
    txt(s, x, y + Inches(0.48), w, h - Inches(0.5), sub, size=11, color=sc, align=PP_ALIGN.CENTER)
# users (one column, two arrows: pages from S3, JSON to API)
node(Inches(0.6), Inches(2.6), Inches(2.3), Inches(2.4), "Browsers",
     ["Organizer laptop", "create · QR · dashboard", "", "Student phone", "scan · check in"])
# aws boundary
box(s, Inches(3.55), Inches(1.75), Inches(9.15), Inches(4.95), None, TEAL, MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.5)
chip(s, Inches(9.6), Inches(1.6), "AWS · ap-southeast-2 (Sydney)", fill=PAPER, color=TEAL, size=11, w=Inches(2.9))
node(Inches(4.0), Inches(2.15), Inches(2.5), Inches(1.15), "Amazon S3", ["Static website", "index · event · checkin"])
node(Inches(4.0), Inches(4.35), Inches(2.5), Inches(1.25), "API Gateway", ["HTTP API · HTTPS", "CORS · 10 rps throttle"])
node(Inches(7.3), Inches(4.35), Inches(2.4), Inches(1.25), "AWS Lambda", ["qroll-api", "Python 3.12 · 256 MB"], fill=INK, line=INK, tc=WHITE, sc=TEAL_SOFT)
node(Inches(10.35), Inches(4.35), Inches(2.1), Inches(1.25), "DynamoDB", ["qroll-attendance", "on-demand · TTL"])
node(Inches(7.3), Inches(2.15), Inches(2.4), Inches(1.15), "IAM role", ["1 table + own logs", "least privilege"], fill=AMBER_SOFT, line=AMBER)
node(Inches(10.35), Inches(2.15), Inches(2.1), Inches(1.15), "CloudWatch", ["logs + metrics"])
arrow(s, Inches(2.9), Inches(2.85), Inches(4.0), Inches(2.72))
arrow(s, Inches(2.9), Inches(4.75), Inches(4.0), Inches(4.97), color=TEAL)
arrow(s, Inches(6.5), Inches(4.97), Inches(7.3), Inches(4.97), color=TEAL)
arrow(s, Inches(9.7), Inches(4.97), Inches(10.35), Inches(4.97), color=TEAL)
arrow(s, Inches(8.5), Inches(3.3), Inches(8.5), Inches(4.35), color=AMBER, dashed=True)
arrow(s, Inches(9.4), Inches(4.35), Inches(10.6), Inches(3.3), color=MUTED, dashed=True)
txt(s, Inches(2.95), Inches(2.4), Inches(1.0), Inches(0.35), "pages", size=10, color=MUTED)
txt(s, Inches(2.95), Inches(5.0), Inches(1.0), Inches(0.5), "JSON / HTTPS", size=10, color=TEAL)
txt(s, Inches(8.6), Inches(3.6), Inches(1.0), Inches(0.35), "assumes", size=10, color=AMBER)
txt(s, Inches(9.72), Inches(5.0), Inches(0.7), Inches(0.35), "txn", size=10, color=TEAL)
txt(s, Inches(3.9), Inches(5.85), Inches(8.6), Inches(0.7),
    "No server is running at any time. Every arrow costs money only when a request actually flows through it.",
    size=13, bold=True, color=TEAL, align=PP_ALIGN.CENTER)

# ============================================================ 6. Check-in flow + rotating token
s = frame("How one check-in works (and why proxies fail)", "Cloud operation")
steps = [("1", "Project", "Dashboard asks Lambda for the current token every 30 s and draws the QR"),
         ("2", "Scan", "Phone opens checkin.html?e=<event>&t=<token>"),
         ("3", "Verify", "Lambda recomputes HMAC for the last 4 windows; no match → 403"),
         ("4", "Commit", "DynamoDB transaction: unique attendee + event open + count++"),
         ("5", "Show", "Dashboard polls every 4 s; the new row flashes on the projector")]
for i, (n, h, b) in enumerate(steps):
    x = Inches(0.6 + i * 2.48)
    box(s, x, Inches(1.85), Inches(2.3), Inches(2.45), WHITE, LINE, MSO_SHAPE.ROUNDED_RECTANGLE)
    c = box(s, x + Inches(0.2), Inches(2.05), Inches(0.55), Inches(0.55), TEAL, None, MSO_SHAPE.OVAL)
    txt(s, x + Inches(0.2), Inches(2.05), Inches(0.55), Inches(0.55), n, size=16, bold=True, color=WHITE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.85), Inches(2.1), Inches(1.4), Inches(0.5), h, size=17, bold=True, color=INK)
    txt(s, x + Inches(0.2), Inches(2.75), Inches(1.95), Inches(1.5), b, size=12.5, color=SLATE)
    if i < 4:
        arrow(s, x + Inches(2.3), Inches(3.08), x + Inches(2.48), Inches(3.08), color=TEAL)
box(s, Inches(0.6), Inches(4.6), Inches(7.4), Inches(2.1), INK, None, MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, Inches(0.9), Inches(4.75), Inches(7.0), Inches(0.35), "ROTATING TOKEN", size=12, bold=True, color=TEAL)
txt(s, Inches(0.9), Inches(5.12), Inches(7.0), Inches(0.6),
    "token = base32( HMAC-SHA256( secret, \"eventId : ⌊now / 30⌋\" ) )[:8]",
    size=15, color=WHITE, font="Courier New")
txt(s, Inches(0.9), Inches(5.7), Inches(7.0), Inches(0.9),
    "The 256-bit secret never leaves DynamoDB/Lambda. A WhatsApp photo of the QR is useless after 2 minutes.",
    size=13, color=RGBColor(0xCB, 0xD5, 0xE1))
rows = [["Attempt", "API answer"], ["Fresh QR", "201 Created"], ["Same reg. no. again", "409 Conflict"],
        ["Old / forged QR", "403 Forbidden"], ["After close", "410 Gone"]]
table(s, Inches(8.3), Inches(4.6), Inches(4.4), rows, [2.4, 2.0], size=13, row_h=0.42)

# ============================================================ 7. Data model
s = frame("Data model: one DynamoDB table does everything", "Cloud operation")
rows = [["PK (partition key)", "SK (sort key)", "Attributes"],
        ["EVENT#7rkhzZ4R", "META", "title, venue, closesAt, closed, count, pinHash, salt, secret, expiresAt"],
        ["EVENT#7rkhzZ4R", "ATT#RA2311003010301", "name, regNo, checkedInAt, expiresAt"],
        ["EVENT#7rkhzZ4R", "ATT#RA2311003010363", "name, regNo, checkedInAt, expiresAt"],
        ["…", "…", "one row per student"]]
t = table(s, Inches(0.6), Inches(1.8), Inches(12.1), rows, [2.6, 3.0, 6.5], size=13, row_h=0.48)
for r in range(1, 5):
    for c in (0, 1):
        t.cell(r, c).text_frame.paragraphs[0].runs[0].font.name = "Courier New"
feats = [("Single-table design", "One Query (PK = EVENT#id, SK begins_with ATT#) returns the full attendance list, sorted by register number."),
         ("Conditional write", "attribute_not_exists(SK) makes each register number unique per event, enforced by the database, not the app."),
         ("ACID transaction", "TransactWriteItems saves the attendee and increments count only if the event is still open. Both happen or neither."),
         ("TTL auto-delete", "expiresAt = close time + 7 days. DynamoDB removes old data for free, so there's no cleanup job.")]
for i, (h, b) in enumerate(feats):
    card(s, Inches(0.6 + i * 3.05), Inches(4.45), Inches(2.85), Inches(2.3), h, b, size=12)

# ============================================================ 8. Security
s = frame("Trust and security controls", "Security (Unit III)")
rows = [["Threat", "Control in QRoll"],
        ["Proxy via forwarded QR photo", "HMAC token rotates every 30 s, valid ≤ 2 min"],
        ["Guessing tokens / PINs", "API throttled to 10 req/s (burst 20); 40-bit token"],
        ["Reading the list without permission", "Organizer PIN: PBKDF2-SHA256 ×100k + salt, constant-time compare"],
        ["Over-privileged backend", "IAM: 5 DynamoDB actions on 1 table + own logs; no delete, no scan"],
        ["Other sites calling the API", "CORS allows only the QRoll website origin"],
        ["Script injection via names", "Server-side validation + HTML escaping in the browser"],
        ["Data kept forever", "DynamoDB TTL deletes event data after 7 days"]]
table(s, Inches(0.6), Inches(1.8), Inches(8.2), rows, [3.3, 4.9], size=13, row_h=0.55)
card(s, Inches(9.1), Inches(1.8), Inches(3.6), Inches(2.4), "Least-privilege IAM",
     ["dynamodb:GetItem · PutItem", "UpdateItem · Query", "ConditionCheckItem", "→ on qroll-attendance only"], size=13, accent=AMBER)
card(s, Inches(9.1), Inches(4.4), Inches(3.6), Inches(2.0), "Known limits",
     ["Someone present can type a friend's reg. no.: needs college SSO (Cognito).", "S3 site is HTTP: add CloudFront + ACM."],
     size=12, accent=RED)

# ============================================================ 9. Practical demonstration: deploy
s = frame("Practical demonstration: deployed with one script", "Practical demonstration · 2 marks")
steps = [("DynamoDB", "create-table · on-demand · TTL"), ("IAM", "create-role · put-role-policy"),
         ("Lambda", "create-function · python3.12"), ("API Gateway", "create-api · 6 routes · stage"),
         ("S3", "mb · website · policy · sync")]
for i, (h, b) in enumerate(steps):
    y = Inches(1.8 + i * 0.86)
    box(s, Inches(0.6), y, Inches(5.6), Inches(0.72), WHITE, LINE, MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, Inches(0.8), y, Inches(0.5), Inches(0.72), str(i + 1), size=20, bold=True, color=TEAL, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.3), y, Inches(1.8), Inches(0.72), h, size=15, bold=True, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(3.05), y, Inches(3.1), Inches(0.72), b, size=12, color=SLATE, anchor=MSO_ANCHOR.MIDDLE, font="Courier New")
txt(s, Inches(0.6), Inches(6.2), Inches(5.6), Inches(0.6),
    [[("./deploy.sh qroll-ra2311003010363 ap-southeast-2", {"font": "Courier New", "color": INK, "bold": True})],
     [("≈ 1 minute · re-runnable · cleanup.sh removes everything", {"size": 11})]], size=13, color=MUTED)
box(s, Inches(6.6), Inches(1.8), Inches(6.1), Inches(4.95), INK, None, MSO_SHAPE.ROUNDED_RECTANGLE)
lines = [("$ ./smoke-test.sh $API", TEAL)] + [(f"  PASS  {t}", WHITE) for t in [
    "create event (HTTP 201)", "wrong PIN rejected (HTTP 401)", "organizer gets QR token (HTTP 200)",
    "check-in (HTTP 201)", "duplicate blocked (HTTP 409)", "forged token rejected (HTTP 403)",
    "attendee list (HTTP 200)", "close event (HTTP 200)", "late check-in rejected (HTTP 410)",
    "unknown event (HTTP 404)"]] + [("", WHITE), ("10 passed, 0 failed", TEAL)]
txt(s, Inches(6.9), Inches(2.0), Inches(5.6), Inches(4.6), [[(l, {"color": c})] for l, c in lines], size=13,
    font="Courier New", spacing=2)

# ============================================================ 10. Demo evidence (app)
s = frame("Live demo: organizer and student views", "Practical demonstration · evidence")
pic(s, "06-live-dashboard-attendees.jpg", Inches(0.6), Inches(1.75), w=Inches(6.6))
txt(s, Inches(0.6), Inches(5.95), Inches(6.6), Inches(0.5),
    "Organizer dashboard: 6 live check-ins, QR token already rotated, closes in 29 min", size=12, color=MUTED)
for i, (f, cap) in enumerate([("04-student-checked-in.jpg", "Checked in"), ("05-duplicate-blocked.jpg", "Duplicate → 409"),
                              ("07-expired-qr-rejected.jpg", "Old QR → 403")]):
    x = Inches(7.45 + i * 1.8)
    pic(s, f, x, Inches(1.75), w=Inches(1.7))
    txt(s, x, Inches(4.47), Inches(1.7), Inches(0.4), cap, size=12, bold=True, color=INK, align=PP_ALIGN.CENTER)
card(s, Inches(7.45), Inches(5.0), Inches(5.25), Inches(1.75), "What the class sees",
     ["Scan → name + reg. no. → ✓ in ~10 s  ·  row flashes on the projector in ≤ 4 s", "Cheating attempts get a clear error message"], size=13)

# ============================================================ 11. Cloud evidence
s = frame("Cloud evidence: the real AWS resources", "Practical demonstration · evidence")
pic(s, "08-dynamodb-items.jpg", Inches(0.6), Inches(1.75), w=Inches(6.0))
txt(s, Inches(0.6), Inches(5.55), Inches(6.0), Inches(0.4), "DynamoDB: 1 META row + 1 ATT# row per student", size=12, bold=True, color=INK)
pic(s, "10-cloudwatch-metrics.jpg", Inches(6.85), Inches(1.75), w=Inches(5.85))
txt(s, Inches(6.85), Inches(5.5), Inches(5.85), Inches(0.4), "CloudWatch: 80 invocations · 0 errors · 100% success", size=12, bold=True, color=INK)
txt(s, Inches(0.6), Inches(6.05), Inches(12.1), Inches(0.7),
    "Cold start ≈ 500 ms on the first request, then 5–40 ms. That's elasticity and measured service seen directly in the metrics.",
    size=13, color=SLATE)

# ============================================================ 12. Features & benefits
s = frame("Features and benefits", "Feature identification · 2 marks")
feats = [("Rotating QR", "Anti-proxy HMAC token, 30 s / 2 min"), ("No duplicates", "Conditional write per reg. no."),
         ("Atomic check-in", "DynamoDB transaction"), ("Live dashboard", "Polling + flashing rows + counter"),
         ("Time-boxed", "Auto close + manual Close button"), ("CSV export", "Straight to Excel / ERP"),
         ("Auto data expiry", "DynamoDB TTL, 7 days"), ("Auto scaling", "Lambda + on-demand DynamoDB"),
         ("Monitoring", "CloudWatch logs & metrics"), ("One-command deploy", "deploy.sh / cleanup.sh")]
for i, (h, b) in enumerate(feats):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 3.75), Inches(1.8 + row * 0.98)
    box(s, x, y, Inches(3.55), Inches(0.84), WHITE, LINE, MSO_SHAPE.ROUNDED_RECTANGLE)
    box(s, x, y, Inches(0.08), Inches(0.84), TEAL)
    txt(s, x + Inches(0.25), y + Inches(0.06), Inches(3.2), Inches(0.4), h, size=14, bold=True, color=INK)
    txt(s, x + Inches(0.25), y + Inches(0.42), Inches(3.2), Inches(0.4), b, size=11.5, color=SLATE)
box(s, Inches(8.3), Inches(1.8), Inches(4.4), Inches(4.75), INK, None, MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, Inches(8.6), Inches(1.95), Inches(3.9), Inches(0.4), "BENEFITS", size=12, bold=True, color=TEAL)
txt(s, Inches(8.6), Inches(2.35), Inches(3.9), Inches(4.1), [
    [("₹0 when idle", {"bold": True, "color": WHITE}), (": no servers running", {})],
    [("Zero ops", {"bold": True, "color": WHITE}), (": no OS, patches, SSH", {})],
    [("Elastic", {"bold": True, "color": WHITE}), (": 10-person lab or 2,000-person fest, same code", {})],
    [("Highly available", {"bold": True, "color": WHITE}), (": runs across 3 AZs by default", {})],
    [("Fast", {"bold": True, "color": WHITE}), (": parallel check-in in seconds vs minutes on paper", {})],
    [("Auditable", {"bold": True, "color": WHITE}), (": server timestamps + CloudWatch logs", {})],
], size=14, color=RGBColor(0xCB, 0xD5, 0xE1), spacing=10)

# ============================================================ 13. Cost
s = frame("Feasibility: cost and limits", "Feature identification · cost")
rows = [["Service (one college / month)", "Usage", "Approx. cost"],
        ["AWS Lambda", "~250k requests × 30 ms", "Free tier"],
        ["API Gateway HTTP API", "~250k requests", "≈ US$0.25"],
        ["DynamoDB on-demand", "~70k writes, ~200k reads", "≈ US$0.15"],
        ["S3 website", "few MB, ~10k GETs", "< US$0.01"],
        ["Total", "", "≈ US$0.40 (≈ ₹35)"]]
t = table(s, Inches(0.6), Inches(1.8), Inches(7.6), rows, [3.0, 2.8, 1.8], size=14, row_h=0.55)
for c in range(3):
    t.cell(5, c).fill.fore_color.rgb = TEAL_SOFT
    for run in t.cell(5, c).text_frame.paragraphs[0].runs:
        run.font.bold = True
txt(s, Inches(0.6), Inches(5.2), Inches(7.6), Inches(1.4),
    [[("Assumption: ", {"bold": True, "color": INK}), ("50 classes/day × 60 students × 22 days ≈ 66k check-ins + dashboard polling.", {})],
     [("Compare: ", {"bold": True, "color": INK}), ("a single t3.small EC2 running 24×7 ≈ US$17/month, and it still needs patching.", {})]],
    size=13, color=SLATE, spacing=8)
card(s, Inches(8.6), Inches(1.8), Inches(4.1), Inches(2.2), "Guardrails used",
     ["API throttling 10 rps", "Logs kept 7 days", "TTL deletes old data", "cleanup.sh removes all"], size=13)
card(s, Inches(8.6), Inches(4.2), Inches(4.1), Inches(2.35), "Current limits",
     ["Polling, not push (WebSocket next)", "PIN, not full login (Cognito next)", "HTTP site (CloudFront next)"], size=13, accent=RED)

# ============================================================ 14. Real-time application
s = frame("Real-time application: a 3,000-person tech fest", "Real-time application · 1 mark")
rows = [["Challenge", "Paper / desks", "QRoll on AWS"],
        ["300 people in 10 min for the keynote", "Queues at 4 desks", "All scan at once; Lambda scales in parallel"],
        ["Busy 1 day, idle 364 days", "Buy / rent for the peak", "Pay per request; ₹0 idle"],
        ["Proxy entries for certificates", "Hard to detect", "Rotating QR + unique reg. no."],
        ["Session reports for certificates", "Manual typing", "CSV per session"],
        ["Privacy after the fest", "Sheets lying around", "TTL deletes after 7 days"]]
table(s, Inches(0.6), Inches(1.8), Inches(7.9), rows, [2.9, 2.0, 3.0], size=12.5, row_h=0.6)
txt(s, Inches(8.85), Inches(1.75), Inches(3.9), Inches(0.4), "Same pattern in industry", size=15, bold=True, color=INK)
txt(s, Inches(8.85), Inches(2.15), Inches(3.9), Inches(1.8), [
    "▸ Conference badge / ticket scanning", "▸ Venue check-in QR (COVID era)", "▸ Restaurant QR ordering",
    "▸ Visitor & parking logs"], size=13, color=SLATE, spacing=6)
txt(s, Inches(8.85), Inches(4.0), Inches(3.9), Inches(0.4), "Scaling path", size=15, bold=True, color=INK)
txt(s, Inches(8.85), Inches(4.4), Inches(3.9), Inches(2.3), [
    [("HTTPS + domain → ", {}), ("CloudFront, ACM", {"bold": True, "color": TEAL})],
    [("Student login → ", {}), ("Cognito", {"bold": True, "color": TEAL})],
    [("Live push → ", {}), ("WebSocket API", {"bold": True, "color": TEAL})],
    [("Daily reports → ", {}), ("EventBridge + SES", {"bold": True, "color": TEAL})],
    [("Analytics → ", {}), ("Athena, QuickSight", {"bold": True, "color": TEAL})]], size=13, color=SLATE, spacing=6)

# ============================================================ 15. Rubric coverage
s = frame("Rubric coverage", "Evaluation")
rows = [["Criterion", "Marks", "Evidence in this case study"],
        ["Tool introduction", "1", "AWS + serverless; Lambda, API Gateway, DynamoDB, S3, IAM, CloudWatch"],
        ["IaaS / PaaS / SaaS exploration", "2", "No IaaS by design; FaaS/PaaS, DBaaS, SaaS tools; responsibility split"],
        ["Practical cloud demonstration", "2", "Live deploy, 10/10 API tests, phone check-in, 409/403/410 shown"],
        ["Features, benefits, applications", "2", "Rotating QR, transactions, TTL, cost ≈ US$0.40/month, use cases"],
        ["Real-time application", "1", "Real AWS reads/writes; live dashboard; tech-fest scenario"],
        ["Viva", "2", "Asked by the evaluator"]]
t = table(s, Inches(0.6), Inches(1.8), Inches(12.1), rows, [3.6, 1.1, 7.4], size=14, row_h=0.62)
for r in range(1, 7):
    t.cell(r, 1).text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
box(s, Inches(0.6), Inches(6.25), Inches(12.1), Inches(0.5), INK, None, MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, Inches(0.9), Inches(6.25), Inches(11.5), Inches(0.5), "TOTAL  10 MARKS", size=14, bold=True, color=WHITE,
    anchor=MSO_ANCHOR.MIDDLE)

# ============================================================ 16. Thank you
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, W, H, INK)
txt(s, Inches(0.8), Inches(0.9), Inches(11), Inches(0.4), "TRY IT  ·  READ IT", size=13, bold=True, color=TEAL)
txt(s, Inches(0.8), Inches(1.4), Inches(11.5), Inches(1.2), "Thank you", size=60, bold=True, color=WHITE)
items = [("Live app", SITE), ("Source + docs + this deck", REPO),
         ("DynamoDB transactions", "docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html"),
         ("DynamoDB TTL", "docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html"),
         ("Lambda + HTTP API", "docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html"),
         ("Pricing", "aws.amazon.com/lambda/pricing · aws.amazon.com/api-gateway/pricing")]
for i, (h, u) in enumerate(items):
    y = Inches(2.9 + i * 0.62)
    txt(s, Inches(0.8), y, Inches(3.4), Inches(0.5), h, size=14, bold=True, color=TEAL)
    txt(s, Inches(4.2), y, Inches(8.5), Inches(0.5), u, size=14, color=WHITE, font="Courier New" if i < 2 else FONT)
txt(s, Inches(0.8), Inches(6.75), Inches(11.5), Inches(0.4),
    "QRoll  ·  Yanamala Uhas Reddy  ·  RA2311003010363  ·  21CSE362T Cloud Computing", size=12,
    color=RGBColor(0x94, 0xA3, 0xB8))

assert len(prs.slides) == TOTAL, len(prs.slides)
cp = prs.core_properties
cp.author = cp.last_modified_by = "Yanamala Uhas Reddy"
cp.title = "QRoll: Serverless QR Attendance on AWS"
cp.subject = "21CSE362T Cloud Computing case study"
out = Path(__file__).with_name("QRoll_Case_Study.pptx")
prs.save(out)
print("saved", out, len(prs.slides), "slides")
