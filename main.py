from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import os
import sys
import logging
from contextlib import contextmanager
from models import Billionaire, Vote, Report, User
from database import Database
from auth import get_current_active_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from utils import calculate_weights
from scrapers.scraper_manager import ScraperManager
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Billionaire Ranking System")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize templates
templates = Jinja2Templates(directory="templates")

# Create database connection manager for serverless environment
@contextmanager
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

# Create scraper manager instance per request
def get_scraper_manager():
    return ScraperManager()

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render the main rankings page"""
    try:
        with get_db() as db:
            logger.info("Fetching billionaires from database")
            billionaires = db.get_billionaires()
            logger.info(f"Retrieved {len(billionaires)} billionaire records")

            weights = calculate_weights(db)
            db.update_billionaire_scores(weights)

            return templates.TemplateResponse(
                "rankings.html",
                {"request": request, "billionaires": sorted(billionaires, key=lambda x: x.overall_score, reverse=True)}
            )
    except Exception as e:
        logger.error(f"Error rendering rankings page: {str(e)}")
        return templates.TemplateResponse(
            "rankings.html",
            {"request": request, "billionaires": [], "error": "Failed to load rankings"}
        )

@app.get("/vote", response_class=HTMLResponse)
async def vote_page(request: Request):
    """Render the voting page"""
    try:
        return templates.TemplateResponse("vote.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering vote page: {str(e)}")
        return templates.TemplateResponse(
            "vote.html",
            {"request": request, "error": "Failed to load voting page"}
        )

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint to get JWT token"""
    if form_data.username == "admin" and form_data.password == "admin":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.get("/rankings", response_model=List[Billionaire])
async def get_rankings():
    """Get ranked list of billionaires"""
    with get_db() as db:
        billionaires = db.get_billionaires()
        weights = calculate_weights(db)
        db.update_billionaire_scores(weights)
        return sorted(billionaires, key=lambda x: x.overall_score, reverse=True)

@app.get("/billionaire/{billionaire_id}", response_model=Billionaire)
async def get_billionaire(billionaire_id: str):
    """Get individual billionaire data"""
    with get_db() as db:
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

    with get_db() as db:
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
    with get_db() as db:
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

@app.post("/update-data/{billionaire_id}")
async def update_billionaire_data(
    billionaire_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """Trigger data update for a specific billionaire"""
    with get_db() as db:
        logger.info(f"Received update request for billionaire {billionaire_id} from user {current_user.username}")

        if not db.get_billionaire(billionaire_id):
            logger.error(f"Billionaire {billionaire_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Billionaire not found"
            )

        scraper_manager = get_scraper_manager()
        background_tasks.add_task(scraper_manager.update_billionaire_data, billionaire_id)
        logger.info(f"Started background update task for billionaire {billionaire_id}")
        return {"message": "Data update started"}

@app.post("/update-all-data")
async def update_all_data(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """Trigger data update for all billionaires"""
    scraper_manager = get_scraper_manager()
    background_tasks.add_task(scraper_manager.update_all_billionaires)
    return {"message": "Full data update started"}

# For local development only
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)