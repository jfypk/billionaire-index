from typing import Dict, Any
from .base_scraper import BaseScraper

class ProPublicaScraperError(Exception):
    pass

class ProPublicaScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.propublica.org"
    
    def get_data(self, identifier: str) -> Dict[str, Any]:
        """
        Get philanthropy and tax practice data from ProPublica
        identifier: Name or ID of the billionaire
        """
        try:
            # Construct search URLs
            philanthropy_url = f"{self.base_url}/search?q={identifier}+foundation+nonprofit"
            tax_url = f"{self.base_url}/search?q={identifier}+taxes"
            
            # Extract content
            philanthropy_content = self.extract_text_content(philanthropy_url)
            tax_content = self.extract_text_content(tax_url)
            
            # Calculate scores
            philanthropy_score = self._calculate_philanthropy_score(philanthropy_content)
            tax_impact = self._assess_tax_practices(tax_content)
            
            return {
                "source": "ProPublica",
                "philanthropy_score": philanthropy_score,
                "tax_practice_impact": tax_impact,
                "timestamp": self.last_updated
            }
        except Exception as e:
            raise ProPublicaScraperError(f"Failed to scrape ProPublica data: {str(e)}")
    
    def _calculate_philanthropy_score(self, content: str) -> float:
        """Calculate philanthropy score (0-20) based on content"""
        score = 10.0  # Default middle score
        
        philanthropy_keywords = {
            "charitable foundation": 2.0,
            "donation": 1.5,
            "nonprofit": 1.0,
            "charitable giving": 2.0,
            "philanthropy": 1.5,
            "grant": 1.0
        }
        
        content_lower = content.lower()
        for keyword, weight in philanthropy_keywords.items():
            if keyword in content_lower:
                score += weight
        
        return min(max(score, 0), 20)
    
    def _assess_tax_practices(self, content: str) -> float:
        """Assess tax practices impact on social score (0-30)"""
        score = 15.0  # Default middle score
        
        # Keywords that affect social responsibility score
        tax_keywords = {
            "tax avoidance": -3.0,
            "offshore account": -2.5,
            "tax haven": -2.5,
            "tax evasion": -4.0,
            "fair tax": 2.0,
            "tax compliance": 2.0
        }
        
        content_lower = content.lower()
        for keyword, impact in tax_keywords.items():
            if keyword in content_lower:
                score += impact
        
        return min(max(score, 0), 30)
