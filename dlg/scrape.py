
from fastapi import Request
from datetime import datetime

from totoms import MessageDestination
from totoms.evt import TotoMessage
from totoms.TotoDelegateDecorator import toto_delegate
from totoms.model.UserContext import UserContext
from totoms.model.ExecutionContext import ExecutionContext

from model.blog import BlogContent
from model.errors import  TotoValidationError
from scraper.extract import CraftBlobTextExtractor
from scraper.scrape import scrape_blog
from storage.kb import KnowledgeBaseStorageFactory, StorageBlogStructure

async def scrape_and_store_blog(blog_url: str, topic_name: str, topic_id: str, user: str, exec_context: ExecutionContext): 
    
    # 1. Scrape the blog
    exec_context.logger.log(exec_context.cid, f'Scraping {blog_url} for topic {topic_name}')
    
    html_content = await scrape_blog(blog_url)
    
    # 2. Extract all the text
    blog_content: BlogContent = CraftBlobTextExtractor(html_content, topic_name).get_content()
    
    # 3. Store the blog content on GCS
    kb_structure: StorageBlogStructure = KnowledgeBaseStorageFactory.get_storage(exec_context).store_blog_content(blog_content)
    
    # 5. Event on PubSub
    msg = TotoMessage(
        timestamp=datetime.now().strftime('%Y%m%d%H%M%S'),
        cid=exec_context.cid,
        id=kb_structure.topic_code,
        type="topicScraped",
        msg=f"The content of topic {kb_structure.topic_code} has been saved in the Knowledge Base",
        data={
            "topicId": topic_id,
            "user": user,
            "topicCode": kb_structure.topic_code, 
            "sections": kb_structure.section_codes,
            "numSections": len(blog_content.sections)
        }
    )
    
    await exec_context.message_bus.publish_message(
        destination=MessageDestination(topic="tometopics"), 
        message=msg
    )
    
    # Return the blog content, the topic id and the blog url
    return {
        "blogContent": blog_content.__dict__,
        "blogUrl": blog_url
    }
    
@toto_delegate
async def extract_blog_content(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
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
    body = await request.json()
    
    # Extract the blog_url from the body
    blog_url = body.get("blogURL")
    blog_type = body.get("blogType")
    topic_name = body.get("topicName", None)
    topic_id = body.get("topicId", None)
    
    # Extract the user from the user context
    user = user_context.email
    
    # Validate that the blog_url is not None, that blog_type is not None, and that blog_type is 'craft'
    if blog_url is None: 
        return TotoValidationError("The blogURL is mandatory").__dict__
    if blog_type is None:
        return TotoValidationError("The blogType is mandatory").__dict__
    if blog_type != 'craft':
        return TotoValidationError("The blogType is unsupported").__dict__
    if topic_name is None:
        return TotoValidationError("The topicName is mandatory").__dict__
    if topic_id is None:
        return TotoValidationError("The topicId is mandatory").__dict__
    
    return await scrape_and_store_blog(blog_url, topic_name, topic_id, user, exec_context)
    