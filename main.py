from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from models import Billionaire, Vote, Report, User
from database import Database
from auth import get_current_active_user
from utils import calculate_weights

app = FastAPI(title="Billionaire Ranking System")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()

@app.get("/")
async def root():
    """API root endpoint with information about available endpoints"""
    return {
        "title": "Billionaire Ranking System API",
        "version": "1.0.0",
        "endpoints": {
            "GET /rankings": "Get ranked list of billionaires",
            "GET /billionaire/{id}": "Get individual billionaire data",
            "POST /vote": "Submit weight adjustments for scoring categories",
            "POST /report": "Submit evidence about a billionaire"
        }
    }

@app.get("/rankings", response_model=List[Billionaire])
async def get_rankings():
    """Get ranked list of billionaires"""
    billionaires = db.get_billionaires()
    weights = calculate_weights(db)
    db.update_billionaire_scores(weights)
    return sorted(billionaires, key=lambda x: x.overall_score, reverse=True)

@app.get("/billionaire/{billionaire_id}", response_model=Billionaire)
async def get_billionaire(billionaire_id: str):
    """Get individual billionaire data"""
    billionaire = db.get_billionaire(billionaire_id)
    if not billionaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billionaire not found"
        )
    return billionaire

@app.post("/vote")
async def submit_vote(
    category: str,
    weight: float,
    current_user: User = Depends(get_current_active_user)
):
    """Submit a vote for category weights"""
    if category not in ["social", "environmental", "political", "philanthropy", "cultural"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category"
        )

    if not 0 <= weight <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be between 0 and 1"
        )

    vote = Vote(
        user_id=current_user.username,
        category=category,
        weight=weight
    )

    db.save_vote(vote)
    weights = calculate_weights(db)
    db.update_billionaire_scores(weights)

    return {"message": "Vote recorded successfully"}

@app.post("/report")
async def submit_report(
    billionaire_id: str,
    evidence: str,
    category: str,
    current_user: User = Depends(get_current_active_user)
):
    """Submit a report about a billionaire"""
    if not db.get_billionaire(billionaire_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billionaire not found"
        )

    report = Report(
        user_id=current_user.username,
        billionaire_id=billionaire_id,
        evidence=evidence,
        category=category
    )

    db.save_report(report)
    return {"message": "Report submitted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)