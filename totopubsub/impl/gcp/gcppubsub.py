import json
import os
from typing import Dict, Any
from totoapicontroller.model.ExecutionContext import ExecutionContext
from totopubsub.model import TotoMessage
from totopubsub.pubsub import PubSub
from google.cloud import pubsub_v1
import google.auth


class GCPPubSub(PubSub):
    
    def __init__(self, exec_context: ExecutionContext): 
        
        self.exec_context = exec_context
        self.cid = exec_context.cid
        
        # Only create one publisher client
        self.credentials, self.project_id = google.auth.default()
        self.publisher = pubsub_v1.PublisherClient(credentials=self.credentials)
    
    def publish_message(self, topic_name: str, message: TotoMessage) -> Dict:
        """
        Publish a message to a GCP Pub/Sub topic.
        
        Args:
            topic_name: The name of the Pub/Sub topic
            message: TotoMessage protocol object containing the message data
            
        Returns:
            str: The message ID of the published message
            
        Raises:
            Exception: If publishing fails
        """
        logger = self.exec_context.logger

        # Convert TotoMessage to dict for serialization
        message_dict = {
            "timestamp": message.timestamp,
            "cid": message.cid,
            "id": message.id,
            "type": message.type,
            "msg": message.msg,
            "data": message.data
        }

        json_message = json.dumps(message_dict)

        logger.log(self.cid, f"Publishing the event [ {message.type} ] on topic [ {topic_name} ] for object with id [ {message.id} ]. The following message is to be published: [ {json_message} ]")

        try:

            topic_path = self.publisher.topic_path(os.getenv('GCP_PID'), topic_name)

            future = self.publisher.publish(topic_path, data=json_message.encode('utf-8'))

            # Only call result() if we need the message ID immediately
            # For fire-and-forget scenarios, consider removing this
            message_id = future.result(timeout=30.0)  # Add timeout to prevent indefinite blocking

            logger.log(self.cid, f"Successfully published the event [ {message.type} ] - Message Id: [ {message_id} ]")

            return {"messageId" : message_id}

        except Exception as e:
            error_msg = f"Publishing the event [ {message.type} ] failed. Error: {str(e)}"
            logger.log(self.cid, error_msg, "error")
            logger.log(self.cid, f"Failed message: [ {json_message} ]", "error")
            raise Exception(error_msg) from e