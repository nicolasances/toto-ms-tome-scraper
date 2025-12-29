
from dataclasses import dataclass
from typing import Type

from totoapicontroller.TotoLogger import TotoLogger
from totoapicontroller.model import TotoEnvironment
from totoapicontroller.model.TotoConfig import TotoConfig


@dataclass
class TotoMicroserviceConfiguration:
    service_name: str
    base_path: str
    environment: TotoEnvironment
    custom_config: Type[TotoConfig] 
    
class TotoMicroservice:
    
    config: TotoMicroserviceConfiguration
    
    def __init__(self, config: TotoMicroserviceConfiguration) -> None:
        self.config = config
        
        # Initialize the Logger
        TotoLogger.get_instance(self.config.service_name)
        
        # Load Configuration
        custom_config = self.config.custom_config(self.config.environment)
        