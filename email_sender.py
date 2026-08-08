import smtplib
from html import escape
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
    """
    Generate a professional HTML email containing job listings.
    """

    if not jobs:
        return """
        <!DOCTYPE html>
        <html>
        <body style="
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        ">

            <div style="
                max-width: 700px;
                margin: auto;
                background: white;
                padding: 25px;
                border-radius: 10px;
            ">

                <h2>Daily Job Search</h2>

                <p>
                    No matching jobs were found today.
                </p>

                <p>
                    The job search agent will try again tomorrow.
                </p>

            </div>

        </body>
        </html>
        """

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    html = """
    <!DOCTYPE html>
    <html>

    <body style="
        margin: 0;
        padding: 0;
        background-color: #f4f6f8;
        font-family: Arial, Helvetica, sans-serif;
    ">

        <div style="
            max-width: 750px;
            margin: 20px auto;
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
        ">

            <!-- Header -->

            <div style="
                padding: 25px;
                background-color: #1f2937;
                color: white;
            ">

                <h1 style="
                    margin: 0;
                    font-size: 24px;
                ">
                    Daily Job Openings
                </h1>

                <p style="
                    margin: 8px 0 0 0;
                    color: #d1d5db;
                ">
                    New opportunities matching your preferences
                </p>

            </div>

            <!-- Summary -->

            <div style="
                padding: 20px 25px;
                border-bottom: 1px solid #e5e7eb;
            ">

                <h3 style="margin-top: 0;">
                    Today's Matches
                </h3>

                <p>
                    <strong>{}</strong>
                    matching jobs found.
                </p>

            </div>

            <!-- Jobs -->

            <div style="padding: 20px 25px;">
    """.format(len(jobs))

    # ---------------------------------------------------------
    # Job cards
    # ---------------------------------------------------------

    for number, job in enumerate(jobs, start=1):

        title = escape(str(job.get("title", "Unknown")))
        company = escape(str(job.get("company", "Unknown")))
        location = escape(str(job.get("location", "Not specified")))
        source = escape(str(job.get("source", "Unknown")))
        posted_date = escape(
            str(job.get("posted_date", "Not available"))
        )
        url = escape(
            str(job.get("url", "#")),
            quote=True
        )

        html += f"""
                <div style="
                    margin-bottom: 20px;
                    padding: 20px;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    background-color: #ffffff;
                ">

                    <h2 style="
                        margin-top: 0;
                        margin-bottom: 10px;
                        font-size: 18px;
                        color: #111827;
                    ">
                        {number}. {title}
                    </h2>

                    <p style="
                        margin: 6px 0;
                        color: #374151;
                    ">
                        <strong>Company:</strong>
                        {company}
                    </p>

                    <p style="
                        margin: 6px 0;
                        color: #374151;
                    ">
                        <strong>Location:</strong>
                        {location}
                    </p>

                    <p style="
                        margin: 6px 0;
                        color: #374151;
                    ">
                        <strong>Source:</strong>
                        {source}
                    </p>

                    <p style="
                        margin: 6px 0 15px 0;
                        color: #374151;
                    ">
                        <strong>Posted:</strong>
                        {posted_date}
                    </p>

                    <a href="{url}"
                       style="
                           display: inline-block;
                           padding: 10px 18px;
                           background-color: #2563eb;
                           color: white;
                           text-decoration: none;
                           border-radius: 6px;
                           font-weight: bold;
                       ">
                        View Job
                    </a>

                </div>
        """

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    html += """

            </div>

            <div style="
                padding: 20px 25px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 12px;
                text-align: center;
            ">

                <p>
                    This email was generated automatically
                    by your Personal Job Search Agent.
                </p>

                <p>
                    GitHub Actions + Python
                </p>

            </div>

        </div>

    </body>

    </html>
    """

    return html


def send_email(jobs):
    """
    Send the job results through Gmail SMTP.
    """

    # ---------------------------------------------------------
    # Validate configuration
    # ---------------------------------------------------------

    if not EMAIL_ADDRESS:
        raise ValueError(
            "EMAIL_ADDRESS is not configured."
        )

    if not EMAIL_PASSWORD:
        raise ValueError(
            "EMAIL_PASSWORD is not configured."
        )

    if not EMAIL_RECIPIENT:
        raise ValueError(
            "EMAIL_RECIPIENT is not configured."
        )

    # ---------------------------------------------------------
    # Generate HTML
    # ---------------------------------------------------------

    html_content = generate_html(jobs)

    # ---------------------------------------------------------
    # Create email
    # ---------------------------------------------------------

    message = MIMEMultipart("alternative")

    message["Subject"] = EMAIL_SUBJECT
    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_RECIPIENT

    # Attach HTML
    message.attach(
        MIMEText(
            html_content,
            "html",
            "utf-8"
        )
    )

    # ---------------------------------------------------------
    # Connect to Gmail
    # ---------------------------------------------------------

    try:

        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=30
        ) as server:

            # Secure the connection
            server.starttls()

            print("Logging into Gmail...")

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            print("Sending email...")

            server.sendmail(
                EMAIL_ADDRESS,
                EMAIL_RECIPIENT,
                message.as_string()
            )

        print("Email sent successfully.")

    except smtplib.SMTPAuthenticationError:

        print(
            "Gmail authentication failed."
        )

        print(
            "Check EMAIL_ADDRESS and "
            "EMAIL_PASSWORD."
        )

        print(
            "Make sure EMAIL_PASSWORD is "
            "a Gmail App Password."
        )

        raise

    except smtplib.SMTPException as error:

        print(
            f"Gmail SMTP error: {error}"
        )

        raise

    except Exception as error:

        print(
            f"Unexpected email error: {error}"
        )

        raise


# -------------------------------------------------------------
# Test email
# -------------------------------------------------------------

if __name__ == "__main__":

    test_jobs = [
        {
            "title": "Software Engineer",
            "company": "Example Company",
            "location": "Hyderabad",
            "source": "Greenhouse",
            "posted_date": "Today",
            "url": "https://example.com"
        },
        {
            "title": "Python Developer",
            "company": "Example Company 2",
            "location": "Bangalore",
            "source": "Lever",
            "posted_date": "Today",
            "url": "https://example.com"
        }
    ]

    send_email(test_jobs)