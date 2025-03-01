from typing import Dict, Any
from .base_scraper import BaseScraper

class CDPScraperError(Exception):
    pass

class CDPScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.cdp.net"

    def get_data(self, identifier: str) -> Dict[str, Any]:
        """
        Get environmental impact data from CDP
        identifier: Name or ID of the billionaire
        """
        try:
            # Construct search URL for company environmental disclosures
            search_url = f"{self.base_url}/en/search/companies?query={identifier}"

            # Extract content
            content = self.extract_text_content(search_url)
            cleaned_content = self.clean_data(content)

            # Process and score the content
            environmental_score = self._calculate_environmental_score(cleaned_content)

            return {
                "source": "CDP",
                "environmental_score": environmental_score,
                "raw_data": cleaned_content,
                "timestamp": self.last_updated
            }
        except Exception as e:
            raise CDPScraperError(f"Failed to scrape CDP data: {str(e)}")

    def _calculate_environmental_score(self, content: str) -> float:
        """
        Calculate environmental score based on CDP data
        Returns a score between 0 and 20

        Scoring criteria:
        - High scores (15-20): Strong climate action and environmental leadership
        - Medium scores (8-14): Some environmental initiatives but room for improvement
        - Low scores (0-7): Poor environmental performance or lack of action
        """
        score = 10.0  # Default middle score

        # Positive environmental initiatives
        positive_keywords = {
            "carbon neutral": 3.0,
            "renewable energy": 2.5,
            "emissions reduction": 2.0,
            "zero waste": 2.0,
            "sustainability": 1.5,
            "climate action": 2.0,
            "biodiversity protection": 2.0,
            "green technology": 1.5,
            "environmental innovation": 1.5,
            "circular economy": 2.0
        }

        # Negative environmental impacts
        negative_keywords = {
            "environmental violation": -3.0,
            "pollution": -2.5,
            "oil spill": -3.0,
            "deforestation": -2.5,
            "fossil fuel": -2.0,
            "carbon intensive": -2.0,
            "waste mismanagement": -2.0,
            "environmental damage": -2.5,
            "climate denial": -3.0
        }

        content_lower = content.lower()
        for keyword, weight in positive_keywords.items():
            if keyword in content_lower:
                score += weight

        for keyword, penalty in negative_keywords.items():
            if keyword in content_lower:
                score += penalty

        return min(max(score, 0), 20)