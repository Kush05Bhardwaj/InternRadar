from fastapi import FastAPI
from db.database import engine, SessionLocal
from db.models import Base, Internship
from scraper.twitter import scrape_twitter
from llm.filter import score_internship
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI Internship Agent Running"}


@app.post("/run-scraper")
def run_scraper():
    db = SessionLocal()

    data = scrape_twitter()

    for item in data:
        score, reason = score_internship(item["description"])

        internship = Internship(
            title=item["title"],
            company=item["company"],
            link=item["link"],
            description=item["description"],
            score=score,
            reason=reason
        )

        db.add(internship)

    db.commit()
    db.close()

    return {"message": f"Added {len(data)} internships with AI scoring"}


@app.get("/internships")
def get_internships():
    db = SessionLocal()
    data = db.query(Internship).all()
    db.close()

    return data