from dataclasses import dataclass
import json
import random
import traceback
from typing import List
import boto3
from botocore.exceptions import ClientError
from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.timeline import Timeline, TimelineDate
from util.kb import KnowledgeBase

# client = boto3.client("bedrock-runtime", region_name="eu-west-1")
client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

class RefreshersGenerator: 
    """This Agent is responsible for generating the refreshers for a given topic and section
    """

    def __init__(self, exec_context: ExecutionContext):
        self.exec_context = exec_context;
        self.logger = exec_context.logger
        self.cid = exec_context.cid
        self.model_id = model_id

    def generate_refresher(self, topic_code: str, section_code: str) -> str: 

        # 1. Load the context
        kb = KnowledgeBase(self.exec_context).get_knowledge(topic_code, section_code)
        
        # 2. Define the First Prompt
        system_prompt = f"""
        You are a specialist on the following topic (here identified by its code): {topic_code}.  
        You are helping a user of our app to refresh (review) the topic you are an expert on. 
        Based on the content of the Knowledge Base, you are asked to provide a refresher to the user to help him (her) better remember the topic.
        This is the KNOWLEDGE BASE:
        ----------------
        {kb}
        ----------------
        Provide a refresher of the topic to the user that will help him (her) better remember the topic. It should be a well explained, detailed, refresher. Add other information about the topic that you might have, as needed.
        Format the refresher using an elegant Wiki formatting, but using HTML. Add extra relevant information that could enhance the reader's knowledge of the topic.
        Follow these rules: 
         - Only provide the HTML code, no other text. 
         - Wrap everything in a <div> with class 'refresher'. 
         - Never use \\n, only use <br>.
        """

        conversation = [
            {
                "role": "user", 
                "content": [{"text": system_prompt}]
            },
        ]
        
        try:
            # Send the message to the model, using a basic inference configuration.
            response = client.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": 4000, "temperature": 0.3, "topP": 0.9},
            )
        
            # Extract and print the response text.
            response_text = response["output"]["message"]["content"][0]["text"]
            
            # Remove all occurrences of \n from the response_text
            response_text = response_text.replace("\n", "")
            
            return response_text
        
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            raise e