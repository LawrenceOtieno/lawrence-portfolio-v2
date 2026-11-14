import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, Response, url_for

app = Flask(__name__)

MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_TO   = "lawrenceit38@gmail.com"

# ── Content data (populated in later steps) ──────────────────────────
projects = []
case_studies = []
testimonials = []
faqs = []

# ── Context: request URL + root available in every template ─────────
@app.context_processor
def inject_globals():
    return {"current_url": request.url, "current_root": request.url_root}

# ── SEO routes ──────────────────────────────────────────────────────
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

# ── Main routes ─────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", projects=projects,
                           case_studies=case_studies,
                           testimonials=testimonials, faqs=faqs)

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