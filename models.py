from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class Billionaire(BaseModel):
    id: str
    name: str
    net_worth: float = Field(..., ge=0)
    social_score: float = Field(..., ge=0, le=30)
    environmental_score: float = Field(..., ge=0, le=20)
    political_score: float = Field(..., ge=0, le=20)
    philanthropy_score: float = Field(..., ge=0, le=20)
    cultural_score: float = Field(..., ge=0, le=10)
    overall_score: float = 0

    @validator('overall_score', pre=True, always=True)
    def calculate_overall_score(cls, v, values):
        weights = {
            'social': 0.3,
            'environmental': 0.2,
            'political': 0.2,
            'philanthropy': 0.2,
            'cultural': 0.1
        }
        
        return (
            values.get('social_score', 0) * weights['social'] +
            values.get('environmental_score', 0) * weights['environmental'] +
            values.get('political_score', 0) * weights['political'] +
            values.get('philanthropy_score', 0) * weights['philanthropy'] +
            values.get('cultural_score', 0) * weights['cultural']
        )

class Vote(BaseModel):
    user_id: str
    category: str
    weight: float = Field(..., ge=0, le=1)
    timestamp: datetime = Field(default_factory=datetime.now)

class Report(BaseModel):
    user_id: str
    billionaire_id: str
    evidence: str
    category: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "pending"

class UserToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None
