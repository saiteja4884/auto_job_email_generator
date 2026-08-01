import os
from dotenv import load_dotenv

# Load .env locally (GitHub Actions provides these as environment variables)
load_dotenv()

# ==========================
# Email Configuration
# ==========================
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", EMAIL_ADDRESS)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# ==========================
# OpenAI (Optional)
# ==========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==========================
# Search APIs (Optional)
# ==========================
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# ==========================
# Job Search Preferences
# ==========================
KEYWORDS = [
    "Software Engineer",
    "Backend Engineer",
    "Python Developer",
    "Data Engineer",
    "Cloud Engineer",
]

LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Remote",
]

EXPERIENCE = "3+ years"

# ==========================
# Company Career Pages (Optional)
# ==========================
COMPANY_CAREER_URLS = [
    "https://careers.google.com/jobs/results/",
    "https://www.amazon.jobs/en/search",
    "https://careers.microsoft.com/",
]

# ==========================
# Database
# ==========================
DATABASE_FILE = "jobs.db"

# ==========================
# Email Subject
# ==========================
EMAIL_SUBJECT = "Daily Job Openings"

# ==========================
# Maximum Jobs in Email
# ==========================
MAX_RESULTS = 25