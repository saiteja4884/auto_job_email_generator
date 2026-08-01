# 🤖 AI Job Search Agent

An automated Python-based job search agent that runs daily using GitHub Actions, searches multiple job sources, filters relevant openings, and sends a personalized email with new opportunities.

## Features

- 🔍 Searches multiple job sources
  - Greenhouse
  - Lever
  - Google Custom Search (optional)
- 📅 Finds newly posted jobs
- 📍 Filters by preferred locations
- 💼 Filters by job titles
- 📧 Sends a daily HTML email
- 🔒 Stores secrets securely using GitHub Secrets
- ⚡ Runs automatically every day with GitHub Actions
- 🧠 Ready for OpenAI integration to rank jobs

---

## Project Structure

```
job-search-agent/
│
├── .github/
│   └── workflows/
│       └── jobs.yml
│
├── config.py
├── search_jobs.py
├── email_sender.py
├── requirements.txt
├── README.md
└── .env
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/job-search-agent.git

cd job-search-agent
```

Create a virtual environment.

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file.

```text
EMAIL_ADDRESS=your_email@gmail.com

EMAIL_PASSWORD=your_app_password

EMAIL_RECIPIENT=your_email@gmail.com

OPENAI_API_KEY=your_openai_api_key

GOOGLE_API_KEY=your_google_api_key

GOOGLE_CSE_ID=your_search_engine_id
```

---

## Gmail Setup

If you're using Gmail SMTP:

1. Enable **2-Step Verification**.
2. Generate an **App Password**.
3. Use the App Password as `EMAIL_PASSWORD`.

Do **not** use your normal Gmail password.

---

## Running Locally

```bash
python search_jobs.py
```

The script will:

1. Search jobs.
2. Filter matching roles.
3. Generate an HTML email.
4. Send it to the configured recipient.

---

## GitHub Actions

Create the workflow:

```
.github/workflows/jobs.yml
```

Example schedule:

```yaml
on:
  schedule:
    - cron: "0 2 * * *"
```

You can also trigger it manually from the **Actions** tab.

---

## GitHub Secrets

Add these secrets in:

```
Settings
→ Secrets and variables
→ Actions
```

| Secret | Description |
|---------|-------------|
| EMAIL_ADDRESS | Gmail address |
| EMAIL_PASSWORD | Gmail App Password |
| OPENAI_API_KEY | OpenAI API key (optional) |
| GOOGLE_API_KEY | Google Custom Search API key |
| GOOGLE_CSE_ID | Search Engine ID |

---

## Supported Job Sources

- Greenhouse
- Lever
- Google Custom Search

Additional sources can be added by creating new search connectors.

---

## Future Enhancements

- Resume matching with AI
- AI job ranking
- Cover letter generation
- SQLite database for duplicate tracking
- Slack / Discord notifications
- Daily job summaries
- Salary filtering
- Remote-only jobs
- Company blacklist
- One-click application dashboard

---

## Tech Stack

- Python
- GitHub Actions
- Requests
- Gmail SMTP
- Google Custom Search API
- OpenAI API (optional)

---

## License

This project is licensed under the MIT License.

---

## Disclaimer

Always comply with the terms of service of the job platforms you access. Prefer official APIs and company career pages over scraping sites that prohibit automated access.

---

## Author

Built to automate daily job searching and deliver relevant opportunities directly to your inbox.