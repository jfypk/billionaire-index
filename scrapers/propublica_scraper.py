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

        # Positive philanthropy indicators
        philanthropy_keywords = {
            "charitable foundation": 2.0,
            "donation": 1.5,
            "nonprofit": 1.0,
            "charitable giving": 2.0,
            "philanthropy": 1.5,
            "grant": 1.0,
            "social impact": 2.0,
            "community support": 1.5,
            "education initiative": 2.0,
            "healthcare access": 2.0
        }

        # Negative indicators
        negative_keywords = {
            "tax deduction": -1.0,
            "publicity stunt": -2.0,
            "misuse of funds": -3.0,
            "investigation": -2.0,
            "controversy": -1.5
        }

        content_lower = content.lower()
        for keyword, weight in philanthropy_keywords.items():
            if keyword in content_lower:
                score += weight

        for keyword, penalty in negative_keywords.items():
            if keyword in content_lower:
                score += penalty

        return min(max(score, 0), 20)

    def _assess_tax_practices(self, content: str) -> float:
        """
        Assess tax practices impact on social score (0-30)
        Heavily penalizes tax avoidance and rewards tax compliance
        """
        score = 15.0  # Default middle score

        # Positive tax practice indicators
        positive_keywords = {
            "fair tax": 3.0,
            "tax compliance": 2.0,
            "transparent reporting": 2.5,
            "public disclosure": 2.0,
            "ethical business": 2.0
        }

        # Negative tax practice indicators
        negative_keywords = {
            "tax avoidance": -4.0,
            "offshore account": -3.5,
            "tax haven": -3.5,
            "tax evasion": -5.0,
            "shell company": -3.0,
            "hidden assets": -3.0,
            "panama papers": -4.0
        }

        content_lower = content.lower()
        for keyword, impact in positive_keywords.items():
            if keyword in content_lower:
                score += impact

        for keyword, penalty in negative_keywords.items():
            if keyword in content_lower:
                score += penalty

        return min(max(score, 0), 30)