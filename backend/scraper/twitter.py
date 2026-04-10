from playwright.sync_api import sync_playwright

def scrape_twitter():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        query = "remote python intern"
        page.goto(f"https://twitter.com/search?q={query}&src=typed_query")

        page.wait_for_timeout(5000)

        tweets = page.locator("article").all()

        for tweet in tweets[:10]:
            try:
                text = tweet.inner_text()
                results.append({
                    "title": "Internship from X",
                    "company": "Unknown",
                    "link": f"https://twitter.com/query/status/{hash(text)}",
                    "description": text
                })
            except:
                continue

        browser.close()

    return results