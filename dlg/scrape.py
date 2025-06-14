
from flask import Request
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext
from totoapicontroller.TotoLogger import TotoLogger

from model.blog import BlogContent
from model.errors import  TotoValidationError
from scraper.extract import CraftBlobTextExtractor
from scraper.scrape import scrape_blog
from storage.gcs import KnowledgeBaseStorage, StorageBlogStructure

def scrape_and_store_blog(blog_url: str, topic_name: str, exec_context: ExecutionContext): 
    
    # 1. Scrape the blog
    exec_context.logger.log(exec_context.cid, f'Scraping {blog_url}')
    
    html_content = scrape_blog(blog_url)
    
    # 2. Extract all the text
    blog_content: BlogContent = CraftBlobTextExtractor(html_content, topic_name).get_content()
    
    # 3. Create a Timeline 
    # timeline: Timeline = TimelineAgent(exec_context=exec_context).extract_timeline(merge_sections(blog_content))
    
    # 4. Store the blog content on GCS
    kb_structure: StorageBlogStructure = KnowledgeBaseStorage(exec_context).store_blog_content(blog_content)
    
    # Return the blog content, the topic id and the blog url
    return {
        "blogContent": blog_content.__dict__,
        # "topicId": str(topic_id), 
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
    