import os
from totoapicontroller.model.singleton import singleton
from totoapicontroller.model.TotoConfig import TotoConfig, CloudProvider

@singleton
class Config(TotoConfig): 
    
    mongo_host: str
    mongo_user: str 
    mongo_pswd: str
    
    def __init__(self):
        super().__init__(cloud_provider=CloudProvider.AWS)
        
        self.logger.log('INIT', 'Loading Mongo-related secrets')
        
        self.mongo_host = self.access_aws_secret_version(f"toto/{self.environment}/mongo-host", "eu-west-1")
        self.mongo_user = self.access_aws_secret_version(f"toto/{self.environment}/toto-ms-tome-agent-mongo-user", "eu-west-1")
        self.mongo_pswd = self.access_aws_secret_version(f"toto/{self.environment}/toto-ms-tome-agent-mongo-pswd", "eu-west-1")
        
        self.logger.log("INIT", "Configuration loaded!")
        
    def get_api_name(self) -> str:
        return "toto-ms-tome-scraper"

    def get_tome_bucket_name(self) -> str: 
        """Retrieves the name of the GCS Bucket that contains all the tome data

        Returns:
            string: the (unique) name of the bucket
        """
        if os.getenv('ENVIRONMENT') == 'prod':
            return 'totolive-tome-bucket'
        
        return 'totoexperiments-tome-bucket'

    
    def get_mongo_connection_string(self): 
        return f"mongodb://{self.mongo_user}:{self.mongo_pswd}@{self.mongo_host}:27017/tome"