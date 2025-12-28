
import traceback
from fastapi import Request
from agent.refresher import RefreshersGenerator
from agent.timeline import TimelineAgent
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.blog import Topic
from model.errors import  TotoValidationError
from model.timeline import Timeline
from scraper.extract import CraftBlobTextExtractor
from scraper.scrape import scrape_blog
from storage.impl.gcs import KnowledgeBaseStorage
from pymongo import MongoClient

from util.section import merge_sections

@toto_delegate(config_class=Config)
async def test_refresher(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    
    config: Config = exec_context.config
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