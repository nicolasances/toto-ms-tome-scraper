
from flask import Request
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.blog import BlogContent
from model.errors import  TotoValidationError
from scraper.extract import CraftBlobTextExtractor
from scraper.scrape import scrape_blog
from storage.kb import KnowledgeBaseStorageFactory, StorageBlogStructure
from totopubsub.model import TotoMessageData
from totopubsub.pubsub import PubSubFactory

def scrape_and_store_blog(blog_url: str, topic_name: str, exec_context: ExecutionContext): 
    
    # 1. Scrape the blog
    exec_context.logger.log(exec_context.cid, f'Scraping {blog_url} for topic {topic_name}')
    
    html_content = scrape_blog(blog_url)
    
    # 2. Extract all the text
    blog_content: BlogContent = CraftBlobTextExtractor(html_content, topic_name).get_content()
    
    # 3. Store the blog content on GCS
    kb_structure: StorageBlogStructure = KnowledgeBaseStorageFactory.get_storage(exec_context).store_blog_content(blog_content)
    
    # 5. Event on PubSub
    event_publisher = PubSubFactory.create_pubsub(exec_context)
    
    msg = TotoMessageData(
        id=kb_structure.topic_code,
        event_name="topicScraped",
        msg=f"The content of topic {kb_structure.topic_code} has been saved in the Knowledge Base",
        data={
            "topicCode": kb_structure.topic_code, 
            "numSections": len(blog_content.sections)
        }
    )
    
    event_publisher.publish_message(topic_name=exec_context.config.topics['tometopics'], message=msg)
    
    # Return the blog content, the topic id and the blog url
    return {
        "blogContent": blog_content.__dict__,
        "blogUrl": blog_url
    }
    
@toto_delegate(config_class=Config)
def extract_blog_content(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    """This API Endpoint extracts the text content of a blog.
    It structures it according to Tome's Knowledge Base structure. 

    Args:
        request (Request): must contain the following body items: 
            - blogURL (str): the URL of the blog to scrape
            - blogType (str): the type of the blog. This can be one of the following:
                * 'craft' for Craft blogs
        user_context (UserContext): _description_
        exec_context (ExecutionContext): _description_

    Returns:
        _type_: _description_
    """
    # Extract the body from the request
    body = request.get_json()
    
    # Extract the blog_url from the body
    blog_url = body.get("blogURL")
    blog_type = body.get("blogType")
    topic_name = body.get("topicName", None)
    
    # Validate that the blog_url is not None, that blog_type is not None, and that blog_type is 'craft'
    if blog_url is None: 
        return TotoValidationError("The blogURL is mandatory").__dict__
    if blog_type is None:
        return TotoValidationError("The blogType is mandatory").__dict__
    if blog_type != 'craft':
        return TotoValidationError("The blogType is unsupported").__dict__
    if topic_name is None:
        return TotoValidationError("The topicName is mandatory").__dict__
    
    return scrape_and_store_blog(blog_url, topic_name, exec_context)
    