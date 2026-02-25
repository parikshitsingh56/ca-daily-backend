from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

START_DATE = datetime(2025, 7, 1)

@app.get("/")
def home():
    return {"message": "CA Daily Backend Running"}

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

    # Temporary response (scraper logic will be added next)
    return {
        "date": date,
        "status": "Backend working. Scraper not added yet."
    }
