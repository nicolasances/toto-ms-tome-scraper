
from datetime import datetime
import traceback
import concurrent
from flask import Request
from agent.timeline import TimelineAgent
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.blog import BlogContent, Topic
from model.errors import  TotoValidationError
from model.timeline import Timeline
from scraper.extract import CraftBlobTextExtractor
from scraper.scrape import scrape_blog
from storage.gcs import KnowledgeBaseStorage, StorageBlogStructure
from pymongo import MongoClient

from util.section import merge_sections
from agent.refresher import RefreshersGenerator

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
    
    config: Config = exec_context.config
    logger = exec_context.logger
    cid = exec_context.cid
    
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
    
    # 1. Scrape the blog
    exec_context.logger.log(exec_context.cid, f'Scraping {blog_url}')
    
    html_content = scrape_blog(blog_url)
    
    # 2. Extract all the text
    blog_content: BlogContent = CraftBlobTextExtractor(html_content, topic_name).get_content()
    
    # 3. Create a Timeline 
    # timeline: Timeline = TimelineAgent(exec_context=exec_context).extract_timeline(merge_sections(blog_content))
    
    # 4. Store the blog content on GCS
    kb_structure: StorageBlogStructure = KnowledgeBaseStorage(exec_context).store_blog_content(blog_content)
            
    # 5. Generate refreshers 
    # def generate_refresher(section_code):
    #     exec_context.logger.log(exec_context.cid, f'Generating refresher for section {section_code}')
    #     refresher_text = RefreshersGenerator(exec_context).generate_refresher(topic_code=kb_structure.topic_code, section_code=section_code)
    #     return {
    #         'topicCode': kb_structure.topic_code, 
    #         'sectionCode': section_code, 
    #         'refersher': refresher_text, 
    #         'generatedOn': datetime.now().strftime('%Y%m%d %H:%M:%S')
    #     }

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(generate_refresher, section_code) for section_code in kb_structure.section_codes]
    #     section_refreshers = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    
    # 6. Save to mongo    
    client = None
    
    # try: 
    #     client = MongoClient(config.get_mongo_connection_string())
        
    #     db = client['tome']
    #     topics = db['topics']
    #     timelines_coll = db['timelines']
    #     refreshers_coll = db['refreshers']
        
    #     topic = Topic(blog_content, blog_url, blog_type)
        
    #     # Save the blog content to the topics collection and save the inserted id
    #     # Overwrite the topic if there's another one with the same topic title in the topics collection
    #     topic_id = topics.update_one({"title": topic.title}, {"$set": topic.to_bson()}, upsert=True).upserted_id
        
    #     # Save the timeline
    #     timelines_coll.delete_many({'topicCode': topic.code})
    #     timelines_coll.insert_many(timeline.to_bson(topic.code))
        
    #     # Save the refreshers
    #     refreshers_coll.delete_many({'topicCode': topic.code})
    #     refreshers_coll.insert_many(section_refreshers)
        
    #     logger.log(cid, f"Saved blog content to MongoDB with Topic ID {str(topic_id)}")
        
    # except Exception as e: 
    #     traceback.print_exc()
    #     return {
    #         "code": 500, 
    #         "msg": "Server Error", 
    #         "error": str(e)
    #     }
    
    # finally: 
    #     if client: 
    #         client.close()
    
    # Return the blog content, the topic id and the blog url
    return {
        "blogContent": blog_content.__dict__,
        # "topicId": str(topic_id), 
        "blogUrl": blog_url
    }