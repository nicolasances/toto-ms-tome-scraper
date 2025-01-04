
from flask import Request
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from scraper.extract import BlobTextExtractor
from scraper.scrape import scrape_blog

@toto_delegate(config_class=Config)
def get_knowledge_from_blog(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    
    # Extract the body from the request
    body = request.get_json()
    
    # Extract the blog_url from the body
    blog_url = body.get("blogURL")
    
    # 1. Scrape the blog
    exec_context.logger.log(exec_context.cid, f'Scraping {blog_url}')
    
    html_content = scrape_blog(blog_url)
    
    # 2. Extract all the text
    text_content = BlobTextExtractor(html_content).get_text()
    
    return {
        "text_content": text_content
    }