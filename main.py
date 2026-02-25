from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

START_DATE = datetime(2025, 7, 1)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(Date)
    content = Column(Text)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "CA Daily Backend Running with DB"}


@app.get("/api/daily")
def fetch_daily(date: str = Query(..., description="Format: YYYY-MM-DD")):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid date format. Use YYYY-MM-DD"}
        )

    if selected_date < START_DATE:
        return JSONResponse(
            status_code=400,
            content={"error": "Data available only from July 2025 onward."}
        )

    db = SessionLocal()

    # Check if already stored
    existing_articles = db.query(Article).filter(Article.date == selected_date.date()).all()

    if existing_articles:
        return {
            "date": date,
            "status": "Loaded from database",
            "articles": [
                {
                    "title": article.title,
                    "content": article.content
                }
                for article in existing_articles
            ]
        }

    # If not stored yet (temporary demo insert)
    demo_article = Article(
        title="Demo Current Affair",
        date=selected_date.date(),
        content="This is a placeholder until scraper is added."
    )

    db.add(demo_article)
    db.commit()

    return {
        "date": date,
        "status": "Stored new data in database",
        "articles": [
            {
                "title": demo_article.title,
                "content": demo_article.content
            }
        ]
    }
