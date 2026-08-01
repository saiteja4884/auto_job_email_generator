import requests
from datetime import datetime
from config import (
    KEYWORDS,
    LOCATIONS,
    GOOGLE_API_KEY,
    GOOGLE_CSE_ID,
)

TODAY = datetime.utcnow().date()


def is_matching_location(location):
    if not location:
        return True

    location = location.lower()

    return any(loc.lower() in location for loc in LOCATIONS)


def search_greenhouse(board):
    """
    Search a Greenhouse job board.
    Example:
    board = "stripe"
    board = "mongodb"
    """

    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

    jobs = []

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        for job in data["jobs"]:

            title = job["title"]

            if not any(k.lower() in title.lower() for k in KEYWORDS):
                continue

            location = job.get("location", {}).get("name", "")

            if not is_matching_location(location):
                continue

            jobs.append({
                "company": board.title(),
                "title": title,
                "location": location,
                "url": job["absolute_url"],
                "source": "Greenhouse",
                "posted_date": TODAY
            })

    except Exception as e:
        print(f"Greenhouse ({board}) failed:", e)

    return jobs


def search_lever(company):
    """
    Search a Lever job board.
    """

    url = f"https://api.lever.co/v0/postings/{company}?mode=json"

    jobs = []

    try:

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        postings = response.json()

        for job in postings:

            title = job["text"]

            if not any(k.lower() in title.lower() for k in KEYWORDS):
                continue

            location = job.get("categories", {}).get("location", "")

            if not is_matching_location(location):
                continue

            jobs.append({
                "company": company.title(),
                "title": title,
                "location": location,
                "url": job["hostedUrl"],
                "source": "Lever",
                "posted_date": TODAY
            })

    except Exception as e:
        print(f"Lever ({company}) failed:", e)

    return jobs


def google_search():
    """
    Uses Google Custom Search API.
    """

    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return []

    jobs = []

    for keyword in KEYWORDS:

        query = f'{keyword} posted today'

        url = (
            "https://www.googleapis.com/customsearch/v1"
            f"?key={GOOGLE_API_KEY}"
            f"&cx={GOOGLE_CSE_ID}"
            f"&q={query}"
        )

        try:

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):

                jobs.append({
                    "company": "",
                    "title": item["title"],
                    "location": "",
                    "url": item["link"],
                    "source": "Google",
                    "posted_date": TODAY
                })

        except Exception as e:
            print("Google Search failed:", e)

    return jobs


def remove_duplicates(jobs):

    unique = {}

    for job in jobs:

        key = (
            job["title"].lower(),
            job["company"].lower(),
            job["location"].lower()
        )

        unique[key] = job

    return list(unique.values())


def search_jobs():

    all_jobs = []

    greenhouse_boards = [
        "stripe",
        "mongodb",
        "datadog",
        "snowflake"
    ]

    lever_companies = [
        "netflix",
        "coinbase",
        "figma"
    ]

    for board in greenhouse_boards:
        all_jobs.extend(search_greenhouse(board))

    for company in lever_companies:
        all_jobs.extend(search_lever(company))

    all_jobs.extend(google_search())

    jobs = remove_duplicates(all_jobs)

    print(f"Found {len(jobs)} jobs")

    return jobs


if __name__ == "__main__":

    jobs = search_jobs()

    for job in jobs:
        print(job)