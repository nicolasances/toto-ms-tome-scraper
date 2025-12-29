
from dataclasses import dataclass
from totoapicontroller import TotoLogger
from totoapicontroller.evt.TotoMessageBus import TotoMessageBus
from totoapicontroller.model.TotoConfig import TotoControllerConfig

@dataclass
class ExecutionContext: 
    
    logger: TotoLogger
    cid: str 
    config: TotoControllerConfig
    message_bus: TotoMessageBus