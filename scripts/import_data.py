import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Add project root to Python path

from database import Database
from database_models import BillionaireModel
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_import_data():
    url = "https://raw.githubusercontent.com/komed3/rtb-api/refs/heads/main/api/list/rtb/2025-01-31"
    logger.info(f"Fetching data from {url}")

    try:
        response = requests.get(url)
        data = response.json()
        logger.info(f"Successfully fetched data. Found {len(data.get('list', []))} billionaires")
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        return

    try:
        db = Database()
        logger.info("Successfully connected to database")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return

    # Clean existing data
    try:
        db.db.query(BillionaireModel).delete()
        db.db.commit()
        logger.info("Cleaned existing data")
    except Exception as e:
        logger.error(f"Error cleaning existing data: {e}")
        db.db.rollback()
        return

    count = 0
    batch_size = 50
    current_batch = []
    seen_ids = set()  # Track used IDs to ensure uniqueness

    for billionaire_data in data.get("list", []):
        try:
            # Get net worth value and convert to float
            net_worth_str = str(billionaire_data.get("networth", "0"))
            # Convert to float (value is already in billions)
            net_worth = float(net_worth_str)

            # Generate unique ID
            base_id = str(billionaire_data.get("rank", ""))
            unique_id = base_id
            suffix = 1
            while unique_id in seen_ids:
                unique_id = f"{base_id}_{suffix}"
                suffix += 1
            seen_ids.add(unique_id)

            # Initialize default scores
            # We'll calculate real scores once we have proper data from scrapers
            billionaire_model = BillionaireModel(
                id=unique_id,  # Using rank as unique ID
                name=billionaire_data.get("name", ""),
                net_worth=net_worth,
                social_score=15.0,  # Default middle scores
                environmental_score=10.0,
                political_score=10.0,
                philanthropy_score=10.0,
                cultural_score=5.0,
                overall_score=10.0  # Will be recalculated based on weights
            )

            current_batch.append(billionaire_model)
            count += 1

            # Process in batches
            if len(current_batch) >= batch_size:
                try:
                    db.db.bulk_save_objects(current_batch)
                    db.db.commit()
                    logger.info(f"Processed {count} records")
                    current_batch = []
                except Exception as e:
                    logger.error(f"Error saving batch: {e}")
                    db.db.rollback()
                    current_batch = []

        except Exception as e:
            logger.error(f"Error processing billionaire data: {e}")
            continue

    # Save any remaining records
    if current_batch:
        try:
            db.db.bulk_save_objects(current_batch)
            db.db.commit()
            logger.info(f"Successfully imported {count} billionaire records")
        except Exception as e:
            logger.error(f"Error committing final batch: {e}")
            db.db.rollback()

if __name__ == "__main__":
    try:
        fetch_and_import_data()
    except Exception as e:
        logger.exception("Unexpected error during import process")