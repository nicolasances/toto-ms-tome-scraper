
from datetime import datetime
import base64
import json
from flask import Request
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from dlg.scrape import extract_blog_content, scrape_and_store_blog
from storage.gcs import KnowledgeBaseStorage

@toto_delegate(config_class=Config)
def on_topic_created(request: Request, user_context: UserContext, exec_context: ExecutionContext): 
    """This API Endpoint reacts to the creation of a topic, received on pubsub on the topic 'tometopics' (event 'topicCreated').
    
    It triggers the extract_blog_content function to extract the text content of a blog.
    """
    
    data = request.get_json()

    if "message" in data: 

        message_data = data["message"]["data"]

        print(f"Received message data: {message_data}")

        decoded_message = json.loads(base64.b64decode(message_data).decode('utf-8'))
        
        print(f"Received Pub/Sub message: {decoded_message}")

        # React to 'topicCreated' event
        # Scrape the blog and store its content in GCS
        if decoded_message["type"] == "topicCreated": 
            
            # Call the function to extract blog content
            return scrape_and_store_blog(decoded_message['data'].get('blogURL'), decoded_message['data'].get('name'), decoded_message['data'].get('user'), exec_context)
        
        elif decoded_message["type"] == "topicDeleted":
            
            # Delete all the content related to the topic
            KnowledgeBaseStorage(exec_context).delete_topic_content(decoded_message['data'].get('name'))
            
            return {"status": "topic content deleted"}
        
    return {"status": "no message to process"}