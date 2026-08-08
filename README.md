# 🤖 Personal Daily Job Search Agent

An automated Python-based job search agent that searches public job listings, filters jobs based on your preferred roles and locations, removes duplicates, and sends a daily email with matching opportunities.

The project runs automatically using **GitHub Actions**.

## ✨ Features

* 🔍 Searches public job listings from:

  * Greenhouse
  * Lever
* 📅 Filters jobs based on posting date
* 💼 Filters jobs by job title/keywords
* 📍 Filters jobs by preferred locations
* 🔄 Removes duplicate jobs
* 📧 Sends a formatted HTML email
* ⏰ Runs automatically every day using GitHub Actions
* 🔐 Keeps email credentials in GitHub Secrets
* 💰 No OpenAI API required
* 💰 No paid search API required
* 🐍 Built entirely with Python

---

# 🏗️ Project Structure

```text
job-search-agent/
│
├── .github/
│   └── workflows/
│       └── jobs.yml
│
├── config.py
├── search_jobs.py
├── email_sender.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🛠️ Technologies Used

* Python 3.12
* GitHub Actions
* Greenhouse public job API
* Lever public job API
* Gmail SMTP
* SQLite
* Python Requests
* Python Dotenv

---

# 🚀 Setup

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/job-search-agent.git
```

Go into the project:

```bash
cd job-search-agent
```

---

# 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

# 3. Install Dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

The project currently uses:

```text
requests==2.32.5
python-dotenv==1.1.1
```

---

# 📧 Gmail Configuration

The application uses Gmail SMTP to send the daily job report.

You should **not use your normal Gmail password**.

Instead, create a Google App Password.

## Create a Gmail App Password

1. Open your Google Account.
2. Enable 2-Step Verification.
3. Open the App Passwords section.
4. Create a new App Password.
5. Copy the generated password.

Use this App Password as:

```text
EMAIL_PASSWORD
```

---

# 🔐 Local Configuration

For local testing, create a file named:

```text
.env
```

in the root of the project.

Example:

```text
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECIPIENT=yourgmail@gmail.com
```

Your structure should be:

```text
job-search-agent/
│
├── .env
├── config.py
├── search_jobs.py
├── email_sender.py
└── ...
```

---

# ⚠️ Never Commit `.env`

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
*.pyc
jobs.db
```

Never upload your Gmail password or App Password to GitHub.

---

# 🔐 GitHub Secrets

When the project runs using GitHub Actions, you don't need to upload `.env`.

Instead, create GitHub Repository Secrets.

Go to:

```text
GitHub Repository
    ↓
Settings
    ↓
Secrets and variables
    ↓
Actions
    ↓
New repository secret
```

Create these secrets:

| Secret            | Value                              |
| ----------------- | ---------------------------------- |
| `EMAIL_ADDRESS`   | Your Gmail address                 |
| `EMAIL_PASSWORD`  | Your Gmail App Password            |
| `EMAIL_RECIPIENT` | Email address receiving the report |

---

# ⚙️ GitHub Actions

The workflow is located at:

```text
.github/workflows/jobs.yml
```

The workflow:

1. Starts a GitHub runner.
2. Downloads the repository.
3. Installs Python.
4. Installs dependencies.
5. Runs `search_jobs.py`.
6. Searches for jobs.
7. Filters the results.
8. Sends the email.
9. Finishes the workflow.

Example workflow:

```yaml
name: Daily Job Search Agent

on:
  schedule:
    - cron: "30 2 * * *"

  workflow_dispatch:

jobs:
  search-and-email:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Search jobs and send email
        env:
          EMAIL_ADDRESS: ${{ secrets.EMAIL_ADDRESS }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_RECIPIENT: ${{ secrets.EMAIL_RECIPIENT }}
        run: python search_jobs.py
```

---

# ⏰ Schedule

The workflow is configured to run at:

```text
02:30 UTC
```

which corresponds to:

```text
08:00 AM IST
```

GitHub Actions uses UTC for scheduled workflows.

The workflow can also be started manually using:

```text
Actions
    ↓
Daily Job Search Agent
    ↓
Run workflow
```

---

# 🔎 Job Search Configuration

Your preferred jobs are configured in `config.py`.

Example:

```python
KEYWORDS = [
    "Software Engineer",
    "Software Developer",
    "Python Developer",
    "Backend Developer",
    "Data Engineer",
    "Data Analyst",
    "Cloud Engineer",
]
```

You can add or remove roles.

For example:

```python
KEYWORDS = [
    "Python Developer",
    "Data Engineer",
    "AWS Engineer",
    "DevOps Engineer",
]
```

---

# 📍 Location Configuration

You can also configure locations:

```python
LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Bengaluru",
    "Chennai",
    "Pune",
    "Remote",
]
```

For example, if you only want Hyderabad and remote jobs:

```python
LOCATIONS = [
    "Hyderabad",
    "Remote",
]
```

---

# 🔎 Supported Job Sources

The current version uses public job-board endpoints from:

* Greenhouse
* Lever

The project does **not** automatically scrape LinkedIn, Indeed, or Naukri.

This is intentional because automated scraping may be restricted by those platforms' terms of service.

Additional sources can be added later using official APIs or publicly available job feeds.

---

# 📧 Email Example

You will receive an email similar to:

```text
Subject: Daily Job Openings

Daily Job Openings

Today's Matches

10 matching jobs found.

1. Software Engineer

Company: Example Company
Location: Hyderabad
Source: Greenhouse
Posted: Today

[View Job]

--------------------------------

2. Python Developer

Company: Example Company 2
Location: Bangalore
Source: Lever
Posted: Today

[View Job]
```

---

# 🧪 Run Locally

To test the complete system:

```bash
python search_jobs.py
```

The program will:

```text
Search jobs
    ↓
Filter keywords
    ↓
Filter locations
    ↓
Filter today's jobs
    ↓
Remove duplicates
    ↓
Generate HTML email
    ↓
Send email
```

---

# 📧 Test Email Separately

You can also test the email functionality:

```bash
python email_sender.py
```

This sends a test email containing sample jobs.

---

# 🗄️ Database

The project uses SQLite to store previously processed jobs.

Database:

```text
jobs.db
```

The database can be used to prevent the same job from being emailed repeatedly.

The database file should not be committed to GitHub.

Add:

```text
jobs.db
```

to `.gitignore`.

---

# 🔒 Security

Never commit these files or values:

```text
.env
Gmail password
Gmail App Password
API keys
jobs.db
```

Use GitHub Secrets for sensitive information.

---

# 💰 Cost

The current architecture is designed to run without paid APIs:

| Component                       | Cost                                   |
| ------------------------------- | -------------------------------------- |
| Python                          | Free                                   |
| GitHub Actions                  | Free within applicable limits          |
| Greenhouse public job endpoints | Free                                   |
| Lever public job endpoints      | Free                                   |
| SQLite                          | Free                                   |
| Gmail SMTP                      | Free within Google's applicable limits |
| OpenAI API                      | Not required                           |

Actual availability and quotas can change, so check the respective service limits before relying on the system for high-volume use.

---

# 🚀 Future Improvements

Possible future features:

* [ ] Search more companies
* [ ] Add Ashby job boards
* [ ] Add additional official job APIs
* [ ] Improve "posted today" detection
* [ ] Track previously emailed jobs
* [ ] Job relevance scoring
* [ ] Resume-based matching
* [ ] Salary filtering
* [ ] Remote-only filtering
* [ ] Company blacklist
* [ ] Job application tracking
* [ ] Google Sheets dashboard
* [ ] Telegram notifications
* [ ] Slack notifications
* [ ] AI-powered job ranking

---

# ⚠️ Disclaimer

This project is intended for personal job searching.

Use official APIs, public job feeds, and publicly available career pages where possible. Always comply with the terms of service and access policies of the websites and services you use.

---

# 📄 License

MIT License

---

# 👨‍💻 Author

Personal Job Search Automation Agent

Built with Python and GitHub Actions.
