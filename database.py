from sqlalchemy.orm import Session
from typing import List, Optional
from models import Billionaire, Vote, Report
from database_models import BillionaireModel, VoteModel, ReportModel
from db_config import get_db
from datetime import datetime

class Database:
    def __init__(self):
        self.db: Session = next(get_db())

    def close(self):
        """Close the database session"""
        if self.db:
            self.db.close()

    def get_billionaires(self) -> List[Billionaire]:
        billionaires = self.db.query(BillionaireModel).all()
        return [
            Billionaire(
                id=b.id,
                name=b.name,
                net_worth=b.net_worth,
                social_score=b.social_score,
                environmental_score=b.environmental_score,
                political_score=b.political_score,
                philanthropy_score=b.philanthropy_score,
                cultural_score=b.cultural_score,
                overall_score=b.overall_score
            ) for b in billionaires
        ]

    def get_billionaire(self, billionaire_id: str) -> Optional[Billionaire]:
        billionaire = self.db.query(BillionaireModel).filter(BillionaireModel.id == billionaire_id).first()
        if not billionaire:
            return None
        return Billionaire(
            id=billionaire.id,
            name=billionaire.name,
            net_worth=billionaire.net_worth,
            social_score=billionaire.social_score,
            environmental_score=billionaire.environmental_score,
            political_score=billionaire.political_score,
            philanthropy_score=billionaire.philanthropy_score,
            cultural_score=billionaire.cultural_score,
            overall_score=billionaire.overall_score
        )

    def save_vote(self, vote: Vote):
        vote_model = VoteModel(
            user_id=vote.user_id,
            category=vote.category,
            weight=vote.weight,
            timestamp=vote.timestamp
        )
        self.db.add(vote_model)
        self.db.commit()

    def save_report(self, report: Report):
        report_model = ReportModel(
            user_id=report.user_id,
            billionaire_id=report.billionaire_id,
            evidence=report.evidence,
            category=report.category,
            timestamp=report.timestamp,
            status=report.status
        )
        self.db.add(report_model)
        self.db.commit()

    def update_billionaire_scores(self, weights: dict):
        billionaires = self.db.query(BillionaireModel).all()
        for b in billionaires:
            b.overall_score = (
                b.social_score * weights['social'] +
                b.environmental_score * weights['environmental'] +
                b.political_score * weights['political'] +
                b.philanthropy_score * weights['philanthropy'] +
                b.cultural_score * weights['cultural']
            )
        self.db.commit()

    def get_votes(self) -> List[dict]:
        votes = self.db.query(VoteModel).all()
        return [
            {
                'category': v.category,
                'weight': v.weight
            } for v in votes
        ]