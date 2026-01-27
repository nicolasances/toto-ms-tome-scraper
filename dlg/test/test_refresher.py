
from fastapi import Request
from agent.refresher import RefreshersGenerator
from config.config import TomeScraperConfig

from totoms.TotoDelegateDecorator import toto_delegate
from totoms.model.UserContext import UserContext
from totoms.model.ExecutionContext import ExecutionContext

@toto_delegate
async def test_refresher(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    
    config: TomeScraperConfig = exec_context.config
    logger = exec_context.logger
    cid = exec_context.cid
    
    data = await request.json()
    
    topic_code = data.get('topicCode')
    section_code = data.get('sectionCode')
    
    llm_response = RefreshersGenerator(exec_context=exec_context).generate_refresher(section_code=section_code, topic_code=topic_code)
    
    # Return the blog content, the topic id and the blog url
    return {
        "response": llm_response
    }