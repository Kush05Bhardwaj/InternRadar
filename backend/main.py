from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from db.database import engine, SessionLocal
from db.models import Base, Internship
from scraper.twitter import scrape_twitter
from llm.filter import score_internship
from scraper.careers import scrape_careers
from llm.email_generator import generate_email

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI Internship Agent Running"}


@app.post("/run-scraper")
def run_scraper():
    db = SessionLocal()

    twitter_data = scrape_twitter()
    careers_data = scrape_careers()

    all_data = twitter_data + careers_data

    for item in all_data:
        existing = db.query(Internship).filter_by(link=item["link"]).first()
        
        if existing:
            continue
            
        description = item["title"] + " " + item["description"]

        score, reason = score_internship(description)

        if score >= 5:
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

    return {"message": f"Added {len(all_data)} internships"}

@app.get("/generate-email/{internship_id}")
def get_email(internship_id: int):
    db = SessionLocal()

    internship = db.query(Internship).filter_by(id=internship_id).first()

    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    email = generate_email(
        internship.title,
        internship.company,
        internship.description
    )

    db.close()

    return {
        "title": internship.title,
        "company": internship.company,
        "email": email
    }

@app.get("/internships")
def get_internships():
    db = SessionLocal()
    data = db.query(Internship).all()
    db.close()

    return data