
import traceback
from flask import Request
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
from evt.publisher import TotoEventPublisher

@toto_delegate(config_class=Config)
def test_pubsub(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    
    config: Config = exec_context.config
    logger = exec_context.logger
    cid = exec_context.cid
    
    publisher = TotoEventPublisher("tometopics", exec_context)
    
    return publisher.publishEvent('azz', 'test', 'ciao', data={"topicCode": "the-bad-popes", "section_code": "ab-sa-s"})
    
    
    