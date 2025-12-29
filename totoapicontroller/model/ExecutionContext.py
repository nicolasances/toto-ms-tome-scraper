
from totoapicontroller import TotoLogger
from totoapicontroller.model.TotoConfig import TotoControllerConfig


class ExecutionContext: 
    
    logger: TotoLogger
    cid: str 
    config: TotoControllerConfig
    
    def __init__(self, config: TotoControllerConfig, logger: TotoLogger, cid: str) -> None:
        self.config = config
        self.logger = logger
        self.cid = cid