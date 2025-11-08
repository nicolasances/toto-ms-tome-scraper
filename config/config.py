import os
from totoapicontroller.model.singleton import singleton
from totoapicontroller.model.TotoConfig import TotoConfig, CloudProvider

@singleton
class Config(TotoConfig): 
    
    topics: dict[str, str]
    
    def __init__(self):

        super().__init__()

        self.topics = {
            "tometopics": self.access_secret_version("tome_topics_topic_name")
        }
        
        self.logger.log("INIT", f"Topics configured: {self.topics}")
        self.logger.log("INIT", "Configuration loaded!")
        
    def get_api_name(self) -> str:
        return "toto-ms-tome-scraper"
    
    def is_path_excluded(self, path: str) -> bool:
        if 'events' in path or 'blogs' in path: 
            return True

        return False

    def get_tome_bucket_name(self) -> str: 
        """Retrieves the name of the GCS Bucket that contains all the tome data

        Returns:
            string: the (unique) name of the bucket
        """
        return f"{os.getenv('GCP_PID')}-tome-bucket"

    