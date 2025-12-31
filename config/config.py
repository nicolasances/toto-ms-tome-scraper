from totoms.model.TotoConfig import TotoControllerConfig
from typing import Optional, Dict

class TomeScraperConfig(TotoControllerConfig):
    """Custom configuration for the Toto Tome Scraper service."""
    
    def get_api_name(self) -> str:
        """Return the API name."""
        return "toto-ms-tome-scraper"
    
    def get_expected_audience(self) -> str:
        """Return the expected JWT audience."""
        return "toto-ms-tome-scraper"
    
    def get_mongo_secret_names(self) -> Optional[Dict[str, str]]:
        """Return MongoDB secret names if service uses MongoDB."""
        return None
