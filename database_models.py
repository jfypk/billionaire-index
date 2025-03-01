from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from datetime import datetime

Base = declarative_base()

class BillionaireModel(Base):
    __tablename__ = "billionaires"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    net_worth = Column(Float, nullable=False)
    social_score = Column(Float, nullable=False)
    environmental_score = Column(Float, nullable=False)
    political_score = Column(Float, nullable=False)
    philanthropy_score = Column(Float, nullable=False)
    cultural_score = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False, default=0)

class VoteModel(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    category = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    billionaire_id = Column(String, ForeignKey('billionaires.id'), nullable=False)
    evidence = Column(String, nullable=False)
    category = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")

    billionaire = relationship("BillionaireModel")
