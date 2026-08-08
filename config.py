import os
from dotenv import load_dotenv

# Load environment variables from .env when running locally
load_dotenv()


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

# Your Gmail address
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")

# Gmail App Password
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Email address where the job report should be sent
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")


# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ============================================================
# JOB SEARCH PREFERENCES
# ============================================================

# Job titles you want to search for
KEYWORDS = [
    "Software Engineer",
    "Software Developer",
    "Python Developer",
    "Backend Developer",
    "Data Engineer",
    "Data Analyst",
    "Cloud Engineer",
]

# Locations you are interested in
LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Bengaluru",
    "Chennai",
    "Pune",
    "Remote",
]


# ============================================================
# JOB SEARCH SETTINGS
# ============================================================

# Maximum number of jobs to include in the email
MAX_RESULTS = 30

# Only include jobs posted today
ONLY_TODAY = True


# ============================================================
# DATABASE
# ============================================================

DATABASE_FILE = "jobs.db"


# ============================================================
# EMAIL
# ============================================================

EMAIL_SUBJECT = "Daily Job Openings"


# ============================================================
# VALIDATION
# ============================================================

def validate_config():
    """
    Check whether required email configuration exists.
    """

    missing = []

    if not EMAIL_ADDRESS:
        missing.append("EMAIL_ADDRESS")

    if not EMAIL_PASSWORD:
        missing.append("EMAIL_PASSWORD")

    if not EMAIL_RECIPIENT:
        missing.append("EMAIL_RECIPIENT")

    if missing:
        raise ValueError(
            "Missing environment variables: "
            + ", ".join(missing)
        )


if __name__ == "__main__":
    validate_config()
    print("Configuration loaded successfully.")