import requests
from bs4 import BeautifulSoup

def scrape_careers():
    results = []

    url = "https://jobs.ashbyhq.com/remote"

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        jobs = soup.find_all("a")

        for job in jobs:
            text = job.get_text()

            if "intern" in text.lower():
                results.append({
                    "title": text.strip(),
                    "company": "Startup",
                    "link": job.get("href"),
                    "description": text.strip()
                })

    except Exception as e:
        print("Careers scrape error:", e)

    return results