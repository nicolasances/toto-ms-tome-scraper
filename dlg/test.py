
from flask import Request
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from scraper.extract import BlobTextExtractor
from scraper.scrape import scrape_blog

@toto_delegate(config_class=Config)
def test(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    
    exec_context.logger.log(exec_context.cid, f"It's working!")
    
    # 1. Scrape the blog
    blog_url = "https://snails-shop-mta.craft.me/RsmQFFdlfFLR0S"  
    
    exec_context.logger.log(exec_context.cid, f'Scraping {blog_url}')
    
    html_content = scrape_blog(blog_url)
    
    # 2. Extract all the text
    text_content = BlobTextExtractor(html_content).get_text()
    
    return {
        "text_content": text_content
    }