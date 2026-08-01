import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_SUBJECT,
)


def generate_html(jobs):
    """Generate HTML email from job list."""

    if not jobs:
        return """
        <html>
            <body>
                <h2>Daily Job Search</h2>
                <p>No matching jobs were found today.</p>
            </body>
        </html>
        """

    html = f"""
    <html>
    <body style="font-family:Arial,sans-serif">

    <h2>Today's Job Openings</h2>

    <p>Total Jobs Found: <b>{len(jobs)}</b></p>

    <hr>
    """

    for i, job in enumerate(jobs, start=1):

        html += f"""
        <h3>{i}. {job['title']}</h3>

        <table cellpadding="5">

        <tr>
            <td><b>Company</b></td>
            <td>{job['company']}</td>
        </tr>

        <tr>
            <td><b>Location</b></td>
            <td>{job['location']}</td>
        </tr>

        <tr>
            <td><b>Source</b></td>
            <td>{job['source']}</td>
        </tr>

        <tr>
            <td><b>Posted</b></td>
            <td>{job['posted_date']}</td>
        </tr>

        <tr>
            <td><b>Apply</b></td>
            <td>
                <a href="{job['url']}">
                    Apply Here
                </a>
            </td>
        </tr>

        </table>

        <hr>
        """

    html += """
    <br>
    <p>
    Generated automatically by your Job Search Agent.
    </p>

    </body>
    </html>
    """

    return html


def send_email(jobs):
    """Send HTML email."""

    message = MIMEMultipart("alternative")

    message["Subject"] = EMAIL_SUBJECT
    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_RECIPIENT

    html = generate_html(jobs)

    message.attach(MIMEText(html, "html"))

    try:

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.sendmail(
                EMAIL_ADDRESS,
                EMAIL_RECIPIENT,
                message.as_string()
            )

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Failed to send email")
        print(e)


if __name__ == "__main__":

    sample_jobs = [
        {
            "title": "Software Engineer",
            "company": "Google",
            "location": "Hyderabad",
            "source": "Greenhouse",
            "posted_date": "2026-08-01",
            "url": "https://example.com/job1"
        },
        {
            "title": "Data Engineer",
            "company": "Amazon",
            "location": "Bangalore",
            "source": "Lever",
            "posted_date": "2026-08-01",
            "url": "https://example.com/job2"
        }
    ]

    send_email(sample_jobs)