import json
import os
from typing import List, Optional
from models import Billionaire, Vote, Report

class Database:
    def __init__(self):
        self.billionaires_file = "data/billionaires.json"
        self.votes_file = "data/votes.json"
        self.reports_file = "data/reports.json"
        self._ensure_data_files()

    def _ensure_data_files(self):
        os.makedirs("data", exist_ok=True)
        for file_path in [self.billionaires_file, self.votes_file, self.reports_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)

    def _read_json(self, file_path: str) -> List[dict]:
        with open(file_path, 'r') as f:
            return json.load(f)

    def _write_json(self, file_path: str, data: List[dict]):
        with open(file_path, 'w') as f:
            json.dump(data, f, default=str)

    def get_billionaires(self) -> List[Billionaire]:
        data = self._read_json(self.billionaires_file)
        return [Billionaire(**b) for b in data]

    def get_billionaire(self, billionaire_id: str) -> Optional[Billionaire]:
        billionaires = self.get_billionaires()
        for b in billionaires:
            if b.id == billionaire_id:
                return b
        return None

    def save_vote(self, vote: Vote):
        votes = self._read_json(self.votes_file)
        votes.append(vote.dict())
        self._write_json(self.votes_file, votes)

    def save_report(self, report: Report):
        reports = self._read_json(self.reports_file)
        reports.append(report.dict())
        self._write_json(self.reports_file, reports)

    def update_billionaire_scores(self, weights: dict):
        billionaires = self.get_billionaires()
        for b in billionaires:
            b.overall_score = (
                b.social_score * weights['social'] +
                b.environmental_score * weights['environmental'] +
                b.political_score * weights['political'] +
                b.philanthropy_score * weights['philanthropy'] +
                b.cultural_score * weights['cultural']
            )
        self._write_json(self.billionaires_file, [b.dict() for b in billionaires])
