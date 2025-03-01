from typing import Dict, Any
from datetime import datetime
import logging
from .opensecrets_scraper import OpenSecretsScraperError, OpenSecretsScraper
from .propublica_scraper import ProPublicaScraperError, ProPublicaScraper
from database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScraperManager:
    def __init__(self):
        self.db = Database()
        self.scrapers = {
            'opensecrets': OpenSecretsScraper(),
            'propublica': ProPublicaScraper(),
        }
    
    async def update_billionaire_data(self, billionaire_id: str) -> Dict[str, Any]:
        """Update billionaire data from all sources"""
        billionaire = self.db.get_billionaire(billionaire_id)
        if not billionaire:
            raise ValueError(f"Billionaire with ID {billionaire_id} not found")
        
        try:
            # Collect data from each source
            political_data = self.scrapers['opensecrets'].get_data(billionaire.name)
            philanthropy_data = self.scrapers['propublica'].get_data(billionaire.name)
            
            # Update scores
            new_scores = {
                'political_score': political_data['political_influence_score'],
                'philanthropy_score': philanthropy_data['philanthropy_score'],
                'social_score': min(philanthropy_data['tax_practice_impact'], 30)
            }
            
            # Log the update
            logger.info(f"Updated scores for {billionaire.name}: {new_scores}")
            
            return new_scores
            
        except (OpenSecretsScraperError, ProPublicaScraperError) as e:
            logger.error(f"Error updating billionaire data: {str(e)}")
            raise
    
    async def update_all_billionaires(self):
        """Update data for all billionaires in the database"""
        billionaires = self.db.get_billionaires()
        for billionaire in billionaires:
            try:
                await self.update_billionaire_data(billionaire.id)
            except Exception as e:
                logger.error(f"Failed to update data for {billionaire.name}: {str(e)}")
