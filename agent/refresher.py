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
# model_id = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
model_id = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'

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
        <task>
        Reformat the given knowledge base while preserving all details. Add any missing relevant information. Present the reformatted information in an elegant Wiki-style HTML format, following these rules:
        - Wrap the entire content in a <div> with class 'refresher'.
        - There must be a h1 tag.
        - Wrap names of people in <span class='highlight-person'></span> tags.
        - Wrap dates in <span class='highlight-date'></span> tags.
        - Only provide the HTML code in your response, without any preamble or explanation.
        - Use <b> tags to highlight important passages or words.
        </task>
        <knowledge_base>
        {kb}
        </knowledge_base>
        <div class='refresher'>
            [Provide the reformatted knowledge base in elegant Wiki-style HTML here, following the given rules]
        </div>
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
                inferenceConfig={"maxTokens": 4096, "temperature": 0.3, "topP": 0.9},
            )
        
            # Extract and print the response text.
            response_text = response["output"]["message"]["content"][0]["text"]
            
            # Remove all occurrences of \n from the response_text
            response_text = response_text.replace("\n", "")
            
            return response_text
        
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            raise e