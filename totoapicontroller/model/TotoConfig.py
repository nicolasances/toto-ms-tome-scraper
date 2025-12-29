from abc import ABC, abstractmethod
from totoapicontroller.TotoLogger import TotoLogger
from totoapicontroller.model.TotoEnvironment import TotoEnvironment
from totoapicontroller.secrets.SecretsManager import SecretsManager

class TotoConfig(ABC): 
    
    jwt_key: str
    jwt_expected_audience: str
    environment: str
    toto_registry_endpoint: str
    mongo_host: str
    
    def __init__(self, environment: TotoEnvironment) -> None:
        
        self.logger = TotoLogger.get_instance()
        
        self.logger.log("INIT", f"Loading Configuration.. Environment: {environment}")
        
        secrets_manager = SecretsManager(environment)

        self.mongo_host = secrets_manager.get_secret("mongo_host")
        self.jwt_key = secrets_manager.get_secret("jwt-signing-key")
        self.jwt_expected_audience = secrets_manager.get_secret("toto-expected-audience")
        self.toto_registry_endpoint = secrets_manager.get_secret("toto-registry-endpoint")
        
    
    @abstractmethod
    def get_api_name(self) -> str: 
        pass
    
    def is_path_excluded(self, path: str) -> bool:
        return False
    

