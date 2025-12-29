
from fastapi import Request
from config.config import TomeScraperConfig

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext
from evt.publisher import TotoEventPublisher

@toto_delegate
async def test_pubsub(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    
    config: TomeScraperConfig = exec_context.config
    logger = exec_context.logger
    cid = exec_context.cid
    
    publisher = TotoEventPublisher("tometopics", exec_context)
    
    return publisher.publishEvent('azz', 'test', 'ciao', data={"topicCode": "the-bad-popes", "section_code": "ab-sa-s"})
    
    
    