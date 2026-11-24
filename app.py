import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, Response, url_for, send_from_directory

app = Flask(__name__)

MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_TO   = "lawrenceit38@gmail.com"

# ── Content data ────────────────────────────────────────────────────
projects = [
    {"name": "Movies Rating Dashboard", "description": "Interactive dashboard analyzing historical movie ratings and audience trends.", "image": "images/projects/moviesr.png", "tags": ["Python", "HTML", "Streamlit"], "link": "https://github.com/LawrenceOtieno/MovieRatingsDashboard"},
    {"name": "Gazebo Indoor Environment Generator", "description": "Automated 3D environment generation for drone simulation and testing.", "image": "images/projects/gazebo.png", "tags": ["Python", "PX4 Autopilot", "Gazebo"], "link": "https://github.com/LawrenceOtieno/gazebo-indoor-gen"},
    {"name": "KRA Nil Automator", "description": "End-to-end automated tax filing pipeline eliminating manual data entry.", "image": "images/projects/automator.png", "tags": ["Python", "Playwright", "Waitress"], "link": "https://github.com/LawrenceOtieno/kra-nil-automator"},
    {"name": "HRM Executive Dashboard", "description": "Executive-level HR analytics dashboard for tracking attrition and retention.", "image": "images/projects/dashboard.png", "tags": ["Python", "Pandas", "Plotly", "Streamlit"], "link": "https://github.com/LawrenceOtieno/hrm-executive-dashboard"},
    {"name": "NYC TLC A/B Testing", "description": "Statistical analysis and hypothesis testing on NYC taxi trip data.", "image": "images/projects/ab-test.png", "tags": ["Python", "SKLearn", "BigQuery"], "link": "#"},
    {"name": "Customer Churn Turnover - ML", "description": "Machine learning model predicting customer churn with 85% accuracy.", "image": "images/projects/churn-rate.png", "tags": ["Python", "Keras"], "link": "#"},
    {"name": "PACE Analytical Framework Blog", "description": "Technical writing on structuring business analytics for maximum impact.", "image": "images/projects/pace.png", "tags": ["WordPress"], "link": "#"},
    {"name": "COVID-19 & Youth Bulge Risk", "description": "Data research analyzing demographic risks and conflict correlations.", "image": "images/projects/covid-youth.png", "tags": ["Excel", "R", "Research"], "link": "#"},
    {"name": "HRM Executive Dashboard (Tableau)", "description": "Tableau version of HR analytics providing interactive visual insights.", "image": "images/projects/hrm.png", "tags": ["Tableau"], "link": "#"},
]

case_studies = [
    {
        "title": "Turning Messy HR Data Into a Simple, Useful Dashboard",
        "summary": "Cleaned conflicting HR records for 500+ employees across 4 cities, then built an executive dashboard from scratch that shows leaders where staff are leaving and why.",
        "tags": ["Python", "Streamlit", "Plotly", "Pandas", "Data Cleaning"],
        "image": "images/case-studies/hrm-case-study-cover.png",
        "view_url": "/case-study/hrm-dashboard",
        "pdf_file": "files/hrm_case_study.pdf",
    },
]

companies = [
    {"name": "Kenya Power & Lighting Company (KPLC)", "city": "Nairobi", "country": "Kenya", "logo": "images/companies/kplc.png", "role": "IT Help Desk Support"},
    {"name": "Kwick Credit", "city": "Nairobi", "country": "Kenya", "logo": "images/companies/kwick-credit.png", "role": "Data Analyst (Contract)"},
    {"name": "Low-Income Financial Transformation (L-IFT)", "city": "Goes", "country": "Netherlands", "logo": "images/companies/l-ift.png", "role": "ICT Support"},
    {"name": "Aesops Ke", "city": "Nairobi", "country": "Kenya", "logo": "images/companies/aesops-ke.png", "role": "Business Analyst"},
]

gallery = [
    {"title": "SimbaNet HRM Dashboard", "tag": "Dashboards", "img": "images/gallery/simbanet-hrm-dashboard.png"},
    {"title": "CineMetrics TV/Movie Intelligence", "tag": "Dashboards", "img": "images/gallery/cinemetrics-tv-movie-intelligence.png"},
    {"title": "The Recommender Interface", "tag": "Machine Learning", "img": "images/gallery/the-recommender-interface.png"},
    {"title": "Gazebo Data Collection Pipeline", "tag": "Pipelines & Automation", "img": "images/gallery/gazebo-data-collection-pipeline.png"},
    {"title": "Nil-Automator", "tag": "Pipelines & Automation", "img": "images/gallery/nil-automator.png"},
    {"title": "Customer Churn Turnover-ML", "tag": "Machine Learning", "img": "images/gallery/customer-churn-turnover-ml.png"},
    {"title": "COVID-19 Fatalities and Risk of Conflicts", "tag": "Analytics", "img": "images/gallery/covid-19-fatalities-risk-of-conflicts.png"},
]

testimonials = [
    {
        "name": "Newton Mbugua",
        "role": "Software Engineer",
        "company": "Aesops ke",
        "quote": "Lawrence is the perfect bridge between business needs and technical execution. He played a vital role in automating our requirements pipeline completely transforming our workflow, letting engineering focus on building software. He is firm, hardworking, and passionate about his work.",
        "rating": 3.5,
        "photo": "images/testimonials/newton-mbugua.png",
        "anonymous": False,
    },
    {
        "name": "John Kamau",
        "role": "Data Team Lead",
        "company": "L-IFT",
        "quote": "Was incredibly reliable in handling critical system support and optimizing our daily data flows. Their dedication to maintaining flawless ICT infrastructure ensured our operations always ran smoothly.",
        "rating": 5,
        "photo": "images/testimonials/john-kamau.png",
        "anonymous": False,
    },
    {
        "name": "Anonymous",
        "role": "Senior Business Analyst",
        "company": "Private",
        "quote": "A brilliant strategist with a sharp eye for workflow bottlenecks. They excelled at gathering stakeholders' chaotic requirements and transforming them into beautifully structured, actionable technical solutions.",
        "rating": 5,
        "initials": "SBA",
        "anonymous": True,
    },
    {
        "name": "Purity Cherono",
        "role": "Communications Specialist",
        "company": "Lilt AI",
        "quote": "Demonstrated outstanding technical precision while documenting complex guidelines for our indigenous language AI models. A highly collaborative engineer who excelled at translating nuanced local variations into structured technical logic.",
        "rating": 5,
        "photo": "images/testimonials/purity-cherono.png",
        "anonymous": False,
    },
    {
        "name": "Anonymous",
        "role": "DevOps & Automation Engineer",
        "company": "Private",
        "quote": "Transformed our slow, manual data entries into automated, highly efficient pipelines. They possessed a deep understanding of software integrations, significantly cutting down our daily operational friction.",
        "rating": 4.5,
        "initials": "DAE",
        "anonymous": True,
    },
    {
        "name": "Norbert Oduor",
        "role": "Data Product Officer",
        "company": "ICEA Lion Group",
        "quote": "Lawrence stepped into our insurance project as a freelancer and instantly simplified massive legacy data into a clear business blueprint. He perfectly bridged our data architecture with actual value, making complex strategy look easy.",
        "rating": 4.0,
        "photo": "images/testimonials/norbert-oduor.png",
        "anonymous": False,
    },
    {
        "name": "Anonymous",
        "role": "Product Manager",
        "company": "Private",
        "quote": "The perfect cross-functional collaborator for systems optimization. Their unique blend of analytical data parsing and automated process mapping completely revitalized our operational efficiency models.",
        "rating": 3.5,
        "initials": "PM",
        "anonymous": True,
    },
    {
        "name": "Kelly Otieno",
        "role": "Peer / Technical Collaborator",
        "company": "",
        "quote": "A master at structuring backend workflows and building highly organized engineering documentation in Jira and Confluence. Their systematic approach to mapping end-to-end operational processes brought absolute clarity to cross-functional teams.",
        "rating": 4.5,
        "photo": "images/testimonials/kelly-otieno.png",
        "anonymous": False,
    },
    {
        "name": "Lynn Ajema",
        "role": "Data Analyst",
        "company": "Aesops ke",
        "quote": "An exceptional analytical thinker who bridges the gap perfectly between technical system requirements and business processes. From managing complex workflows to optimizing SAP modules, their documentation and reporting are top-tier.",
        "rating": 5,
        "photo": "images/testimonials/lynn-ajema.png",
        "anonymous": False,
    },
]

faqs = [
    {
        "question": "What is your primary technical stack?",
        "answer": "I specialize in Python (its libraries and frameworks), Excel, Power BI, SQL, and automation & integration tools. For web apps and dashboards, I frequently use Streamlit, Plotly, and Flask.",
    },
    {
        "question": "Are you open to contract or full-time remote opportunities?",
        "answer": "Yes, I am fully equipped for full-time, remote, hybrid, and on-site roles, as well as project-based consultancies.",
    },
    {
        "question": "How do you handle data privacy and security?",
        "answer": "When building dashboards (like the HRM Executive Dashboard), I ensure PII is masked by default. Access to sensitive data requires authentication, and I always follow the principle of least privilege when connecting to production databases.",
    },
    {
        "question": "Do you only build dashboards, or do you also handle backend data pipelines?",
        "answer": "Both. I build the entire pipeline: from writing Python scripts to extract and clean raw data (ETL), to automating the workflows using Airflow or GitHub Actions, to building the final visualization layer in Streamlit or Power BI.",
    }
]

@app.context_processor
def inject_globals():
    return {"current_url": request.url, "current_root": request.url_root}

@app.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": url_for("index", _external=True), "priority": "1.0", "freq": "weekly"},
        {"loc": url_for("case_study_hrm", _external=True), "priority": "0.8", "freq": "monthly"},
    ]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{p['loc']}</loc>")
        lines.append(f"    <lastmod>{date.today().isoformat()}</lastmod>")
        lines.append(f"    <changefreq>{p['freq']}</changefreq>")
        lines.append(f"    <priority>{p['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return Response("\n".join(lines), mimetype="application/xml")

@app.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /contact\n\n"
        f"Sitemap: {url_for('sitemap', _external=True)}\n",
        mimetype="text/plain",
    )

@app.route("/")
def index():
    return render_template("index.html", projects=projects,
                           case_studies=case_studies,
                           testimonials=testimonials, faqs=faqs,
                           companies=companies, gallery=gallery)

@app.route("/googlefdf100a20e9b9414.html")
def google_verification():
    return send_from_directory("static", "googlefdf100a20e9b9414.html")

@app.route("/case-study/hrm-dashboard")
def case_study_hrm():
    return render_template("case-study/hrm-dashboard.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or request.form
    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    phone   = (data.get("phone")   or "").strip()
    message = (data.get("message") or "").strip()

    if not all([name, email, message]):
        return jsonify({"ok": False, "error": "Please fill in all required fields."}), 400
    if not MAIL_PASS:
        app.logger.warning("MAIL_PASS not set.")
        return jsonify({"ok": False, "error": "Server mail not configured."}), 500

    try:
        send_email(name, email, phone, message)
        return jsonify({"ok": True, "message": "Message sent!"})
    except Exception as exc:
        app.logger.exception("Failed to send email: %s", exc)
        return jsonify({"ok": False, "error": "Failed to send email."}), 500


def send_email(name, email, phone, message):
    msg = MIMEMultipart("alternative")
    msg["Subject"]  = f"Portfolio Contact: {name}"
    msg["From"]     = MAIL_USER
    msg["To"]       = MAIL_TO
    msg["Reply-To"] = email

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif;color:#0B3B3C;">
      <h2 style="color:#F28A1C;">New message from your portfolio</h2>
      <table cellpadding="8" style="border-collapse:collapse;width:100%;max-width:600px;">
        <tr><td style="font-weight:bold;width:100px;">Name</td><td>{name}</td></tr>
        <tr style="background:#F6F8F9;"><td style="font-weight:bold;">Email</td><td><a href="mailto:{email}">{email}</a></td></tr>
        <tr><td style="font-weight:bold;">Phone</td><td>{phone}</td></tr>
        <tr style="background:#F6F8F9;"><td style="font-weight:bold;vertical-align:top;">Message</td>
            <td style="white-space:pre-wrap;">{message}</td></tr>
      </table>
      <p style="margin-top:20px;font-size:12px;color:#888;">Sent from lawrenceotieno.stredata.com</p>
    </body></html>
    """
    text_body = f"New portfolio contact\n\nName:    {name}\nEmail:   {email}\nPhone:   {phone}\nMessage:\n{message}\n"
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, MAIL_TO, msg.as_string())

if __name__ == "__main__":
    app.run(debug=True)