import requests

def run_daily():
    try:
        res = requests.post("http://127.0.0.1:8000/run-scraper")
        print("Scraper run:", res.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    run_daily()