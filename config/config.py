import os
from totoapicontroller.model.singleton import singleton
from totoapicontroller.model.TotoConfig import TotoConfig, CloudProvider

@singleton
class Config(TotoConfig): 
    
    def __init__(self):
        super().__init__(cloud_provider=os.getenv('HYPERSCALER') == 'aws' ? CloudProvider.AWS : CloudProvider.GCP)
        
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

    