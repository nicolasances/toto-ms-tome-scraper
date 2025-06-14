
from datetime import datetime
import base64
import json
from flask import Request
from config.config import Config

from totoapicontroller.TotoDelegateDecorator import toto_delegate
from totoapicontroller.model.UserContext import UserContext
from totoapicontroller.model.ExecutionContext import ExecutionContext

from dlg.scrape import extract_blog_content

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

        # KUD Uploaded Event Handling
        if decoded_message["type"] == "topicCreated": 
            
            # Create a forged request to pass the blog URL and type
            forged_request = Request(
                method='POST',
                data=json.dumps({
                    "blogURL": decoded_message.data.get("blogURL"),
                    "blogType": "craft", 
                    "topicName": decoded_message.data.get("name", None)
                }),
                headers={'Content-Type': 'application/json'}
            )

            # Call the function to extract blog content
            return extract_blog_content(forged_request, user_context, exec_context)
        
    return {"status": "no message to process"}