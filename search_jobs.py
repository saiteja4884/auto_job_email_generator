import requests
from datetime import datetime, timezone
from config import KEYWORDS, LOCATIONS, MAX_RESULTS, ONLY_TODAY
from email_sender import send_email


# ============================================================
# CONFIGURATION
# ============================================================

# Greenhouse companies
# The value is the company's Greenhouse board name.
GREENHOUSE_COMPANIES = [
    "stripe",
    "mongodb",
    "datadog",
    "snowflake",
    "airbnb",
    "coinbase",
]

# Lever companies
# The value is the company's Lever site name.
LEVER_COMPANIES = [
    "netflix",
    "figma",
    "coinbase",
]


# ============================================================
# DATE FUNCTIONS
# ============================================================

def get_today():
    """
    Return today's date in UTC.

    GitHub Actions runs in UTC, so using UTC keeps
    the workflow consistent.
    """
    return datetime.now(timezone.utc).date()


TODAY = get_today()


def is_today(date_string):
    """
    Check whether a timestamp belongs to today.
    """

    if not date_string:
        return False

    try:
        # Example:
        # 2026-08-08T10:30:00Z

        date_string = date_string.replace("Z", "+00:00")

        date_value = datetime.fromisoformat(date_string)

        return date_value.date() == TODAY

    except Exception:
        return False


# ============================================================
# KEYWORD FILTER
# ============================================================

def matches_keyword(title):
    """
    Check whether the job title matches one of
    the configured keywords.
    """

    if not title:
        return False

    title_lower = title.lower()

    return any(
        keyword.lower() in title_lower
        for keyword in KEYWORDS
    )


# ============================================================
# LOCATION FILTER
# ============================================================

def matches_location(location):
    """
    Check whether the job location matches one of
    the configured locations.
    """

    # If no location is available, don't automatically reject it.
    if not location:
        return True

    location_lower = location.lower()

    return any(
        loc.lower() in location_lower
        for loc in LOCATIONS
    )


# ============================================================
# GREENHOUSE
# ============================================================

def search_greenhouse(company):
    """
    Search jobs from a Greenhouse public job board.
    """

    url = (
        f"https://boards-api.greenhouse.io/v1/boards/"
        f"{company}/jobs"
    )

    jobs = []

    print(f"\nSearching Greenhouse: {company}")

    try:

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        for job in data.get("jobs", []):

            title = job.get("title", "")

            location = (
                job.get("location", {})
                .get("name", "")
            )

            updated_at = job.get("updated_at")

            # -----------------------------
            # Keyword filter
            # -----------------------------

            if not matches_keyword(title):
                continue

            # -----------------------------
            # Location filter
            # -----------------------------

            if not matches_location(location):
                continue

            # -----------------------------
            # Today filter
            # -----------------------------

            if ONLY_TODAY:

                if not is_today(updated_at):
                    continue

            jobs.append({
                "company": company.title(),
                "title": title,
                "location": location,
                "url": job.get("absolute_url", ""),
                "source": "Greenhouse",
                "posted_date": updated_at or ""
            })

    except requests.exceptions.RequestException as error:

        print(
            f"Greenhouse error for {company}: "
            f"{error}"
        )

    except Exception as error:

        print(
            f"Unexpected Greenhouse error for "
            f"{company}: {error}"
        )

    print(
        f"Found {len(jobs)} matching jobs "
        f"from {company}"
    )

    return jobs


# ============================================================
# LEVER
# ============================================================

def search_lever(company):
    """
    Search jobs from a Lever public job board.
    """

    url = (
        f"https://api.lever.co/v0/postings/"
        f"{company}?mode=json"
    )

    jobs = []

    print(f"\nSearching Lever: {company}")

    try:

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        postings = response.json()

        for job in postings:

            title = job.get("text", "")

            categories = job.get(
                "categories",
                {}
            )

            location = categories.get(
                "location",
                ""
            )

            created_at = job.get("createdAt")

            # -----------------------------
            # Keyword filter
            # -----------------------------

            if not matches_keyword(title):
                continue

            # -----------------------------
            # Location filter
            # -----------------------------

            if not matches_location(location):
                continue

            # -----------------------------
            # Today filter
            # -----------------------------

            if ONLY_TODAY:

                if created_at:

                    try:

                        created_date = (
                            datetime.fromtimestamp(
                                created_at / 1000,
                                tz=timezone.utc
                            ).date()
                        )

                        if created_date != TODAY:
                            continue

                    except Exception:

                        continue

                else:

                    continue

            jobs.append({
                "company": company.title(),
                "title": title,
                "location": location,
                "url": job.get("hostedUrl", ""),
                "source": "Lever",
                "posted_date": (
                    datetime.fromtimestamp(
                        created_at / 1000,
                        tz=timezone.utc
                    ).isoformat()
                    if created_at
                    else ""
                )
            })

    except requests.exceptions.RequestException as error:

        print(
            f"Lever error for {company}: "
            f"{error}"
        )

    except Exception as error:

        print(
            f"Unexpected Lever error for "
            f"{company}: {error}"
        )

    print(
        f"Found {len(jobs)} matching jobs "
        f"from {company}"
    )

    return jobs


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(jobs):
    """
    Remove duplicate jobs using title, company,
    location and URL.
    """

    unique_jobs = {}

    for job in jobs:

        key = (
            job.get("title", "").strip().lower(),
            job.get("company", "").strip().lower(),
            job.get("location", "").strip().lower(),
            job.get("url", "").strip().lower()
        )

        if key not in unique_jobs:

            unique_jobs[key] = job

    return list(unique_jobs.values())


# ============================================================
# SORT JOBS
# ============================================================

def sort_jobs(jobs):
    """
    Sort jobs alphabetically by company and title.
    """

    return sorted(
        jobs,
        key=lambda job: (
            job.get("company", ""),
            job.get("title", "")
        )
    )


# ============================================================
# MAIN SEARCH FUNCTION
# ============================================================

def search_jobs():

    print("=" * 60)
    print("DAILY JOB SEARCH AGENT")
    print("=" * 60)

    print(f"Today's date: {TODAY}")

    all_jobs = []

    # -----------------------------
    # Search Greenhouse
    # -----------------------------

    for company in GREENHOUSE_COMPANIES:

        jobs = search_greenhouse(company)

        all_jobs.extend(jobs)

    # -----------------------------
    # Search Lever
    # -----------------------------

    for company in LEVER_COMPANIES:

        jobs = search_lever(company)

        all_jobs.extend(jobs)

    print("\nTotal jobs before duplicate removal:")
    print(len(all_jobs))

    # -----------------------------
    # Remove duplicates
    # -----------------------------

    all_jobs = remove_duplicates(all_jobs)

    print("Total jobs after duplicate removal:")
    print(len(all_jobs))

    # -----------------------------
    # Sort
    # -----------------------------

    all_jobs = sort_jobs(all_jobs)

    # -----------------------------
    # Limit results
    # -----------------------------

    all_jobs = all_jobs[:MAX_RESULTS]

    print(f"\nJobs to be emailed: {len(all_jobs)}")

    return all_jobs


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    try:

        jobs = search_jobs()

        # Print results for GitHub Actions logs
        print("\n" + "=" * 60)
        print("JOB RESULTS")
        print("=" * 60)

        for number, job in enumerate(
            jobs,
            start=1
        ):

            print(
                f"\n{number}. "
                f"{job['title']}"
            )

            print(
                f"   Company: "
                f"{job['company']}"
            )

            print(
                f"   Location: "
                f"{job['location']}"
            )

            print(
                f"   Source: "
                f"{job['source']}"
            )

            print(
                f"   URL: "
                f"{job['url']}"
            )

        # -----------------------------
        # Send email
        # -----------------------------

        print("\nSending email...")

        send_email(jobs)

        print("\nJob search completed successfully.")

    except Exception as error:

        print(
            f"\nJob search failed: {error}"
        )

        raise