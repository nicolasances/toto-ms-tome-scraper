
import base64
from enum import Enum
import json
from fastapi import Request
from config.config import TomeScraperConfig

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from dlg.scrape import scrape_and_store_blog
from storage.impl.gcs import KnowledgeBaseStorage

class TopicEvent(Enum):
    TOPIC_CREATED = "topicCreated"
    TOPIC_REFRESHED = "topicRefreshed"
    TOPIC_DELETED = "topicDeleted"

@toto_delegate(config_class=TomeScraperConfig)
async def on_topic_event(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    """This API Endpoint reacts to the creation of a topic, received on pubsub on the topic 'tometopics' (event 'topicCreated').
    
    It triggers the extract_blog_content function to extract the text content of a blog.
    """
    
    data = await request.json()

    if "message" in data: 

        message_data = data["message"]["data"]

        decoded_message = json.loads(base64.b64decode(message_data).decode('utf-8'))
    
        logger = exec_context.logger
        cid = decoded_message.get('cid')
        exec_context.cid = cid
        
        logger.log(cid, f"Received Pub/Sub message: {decoded_message}")

        # React to 'topicCreated' event
        # Scrape the blog and store its content in GCS
        if decoded_message["type"] == TopicEvent.TOPIC_CREATED.value or decoded_message["type"] == TopicEvent.TOPIC_REFRESHED.value: 
            
            # Call the function to extract blog content
            return scrape_and_store_blog(decoded_message['data'].get('blogURL'), decoded_message['data'].get('name'), decoded_message.get('id'), decoded_message['data'].get('user'), exec_context)
        
        elif decoded_message["type"] == TopicEvent.TOPIC_DELETED.value:
            
            # Delete all the content related to the topic
            KnowledgeBaseStorage(exec_context).delete_topic_content(decoded_message['data'].get('name'))
            
            return {"status": "topic content deleted"}
        
        logger.log(cid, f"Event {decoded_message['type']} is not handled by this service. Skipping.")
        
    return {"status": "no message to process"}