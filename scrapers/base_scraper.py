from abc import ABC, abstractmethod
from typing import Dict, Any
import trafilatura
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self):
        self.last_updated = datetime.now()

    @abstractmethod
    def get_data(self, identifier: str) -> Dict[str, Any]:
        """Get data for a specific billionaire"""
        pass

    def extract_text_content(self, url: str) -> str:
        """Extract clean text content from a webpage"""
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded) or ""
        return ""

    def clean_data(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        # Remove extra whitespace
        text = " ".join(text.split())
        return text
