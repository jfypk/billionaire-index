from typing import Dict, Any
from .base_scraper import BaseScraper

class GlassdoorScraperError(Exception):
    pass

class GlassdoorScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.glassdoor.com"
    
    def get_data(self, identifier: str) -> Dict[str, Any]:
        """
        Get employee satisfaction and company culture data from Glassdoor
        identifier: Name or ID of the billionaire
        """
        try:
            # Construct search URL for company reviews
            search_url = f"{self.base_url}/Search/results.htm?keyword={identifier}"
            
            # Extract content
            content = self.extract_text_content(search_url)
            cleaned_content = self.clean_data(content)
            
            # Calculate worker treatment score
            worker_treatment_score = self._calculate_worker_treatment_score(cleaned_content)
            
            return {
                "source": "Glassdoor",
                "worker_treatment_score": worker_treatment_score,
                "raw_data": cleaned_content,
                "timestamp": self.last_updated
            }
        except Exception as e:
            raise GlassdoorScraperError(f"Failed to scrape Glassdoor data: {str(e)}")
    
    def _calculate_worker_treatment_score(self, content: str) -> float:
        """
        Calculate worker treatment score based on Glassdoor reviews
        Returns a score between 0 and 30 (contributes to social score)
        """
        score = 15.0  # Default middle score
        
        # Keywords related to worker treatment and company culture
        worker_keywords = {
            "work-life balance": 2.0,
            "fair compensation": 2.0,
            "benefits": 1.5,
            "career growth": 1.5,
            "positive culture": 1.5,
            "diversity": 1.5,
            "employee wellbeing": 1.0,
            "workplace safety": 1.0,
            "professional development": 1.0
        }
        
        content_lower = content.lower()
        for keyword, weight in worker_keywords.items():
            if keyword in content_lower:
                score += weight
        
        return min(max(score, 0), 30)
