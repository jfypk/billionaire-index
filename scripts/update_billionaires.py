import json
import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
import logging

# Add parent directory to path to import from parent
sys.path.append(str(Path(__file__).parent.parent))

from database_models import Base, BillionaireModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_net_worth(net_worth_str):
    """Convert net worth string to float value in billions"""
    try:
        return float(net_worth_str.replace('$', '').replace(' billion', ''))
    except ValueError as e:
        logger.error(f"Error converting net worth: {net_worth_str}")
        raise e

def update_billionaires():
    """Update billionaire data from JSON file"""
    try:
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        # Create database engine and session
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        logger.info("Reading billionaire data from JSON file...")
        with open('attached_assets/billionaires-json.json', 'r') as f:
            data = json.load(f)

        # Process each billionaire
        for billionaire_data in data['billionaires']:
            try:
                # Clean and prepare data
                name = billionaire_data['name']
                net_worth = clean_net_worth(billionaire_data['netWorth'])

                # Create new billionaire with default scores
                billionaire = BillionaireModel(
                    id=str(uuid.uuid4()),  # Generate unique ID
                    name=name,
                    net_worth=net_worth,
                    social_score=15.0,  # Default mid-range scores
                    environmental_score=10.0,
                    political_score=10.0,
                    philanthropy_score=10.0,
                    cultural_score=5.0,
                    overall_score=0.0  # Will be calculated by the model
                )
                session.add(billionaire)
                logger.info(f"Added billionaire: {name} with net worth: ${net_worth}B")

            except Exception as e:
                logger.error(f"Error processing billionaire {name}: {str(e)}")
                session.rollback()
                continue

        # Commit changes
        logger.info("Committing changes to database...")
        session.commit()
        logger.info("Successfully updated billionaire data")

    except Exception as e:
        logger.error(f"Failed to update billionaires: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    update_billionaires()