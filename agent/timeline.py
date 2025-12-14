from dataclasses import dataclass
import json
import random
import traceback
from typing import List
import boto3
from botocore.exceptions import ClientError
from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.timeline import Timeline, TimelineDate

# client = boto3.client("bedrock-runtime", region_name="eu-west-1")
client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

class TimelineAgent: 
    """This Agent is responsible for extracting a timeline from a knowledge base
    """

    def __init__(self, exec_context: ExecutionContext):
        self.exec_context = exec_context;
        self.logger = exec_context.logger
        self.cid = exec_context.cid

    def extract_timeline(self, corpus: str) -> Timeline: 

        # 1. Define the Prompt
        system_prompt = f"""
        You have to extract a timeline from the corpus that follows. 
        A timeline is a series of events, consituted of a date and the related event. 
        This is the corpus:
        ----------------
        {corpus}
        ----------------
        Extract all the dates in the corpus with a very short description (max 10 words) of the event. 
        Return the result in a JSON format, as an array of objects, each object having a 'date' field and a 'events' fields. 
        - The 'date' field has to be a year. Not a range, just a year, as an integer.
        - The 'events' field contains all the events happening on that date. 
        Each string in the 'events' array must be short (max 10 words). 
        Do not add extra text, only return a JSON. 
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
                modelId=model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": 5000, "temperature": 0, "topP": 0.9},
            )
        
            # Extract and print the response text.
            response_text = response["output"]["message"]["content"][0]["text"]
        
            # Parse as a JSON
            timeline_json = json.loads(response_text)
            
            # Crate the TimelineDate[]
            timeline_dates = [TimelineDate(item['date'], item['events']) for item in timeline_json]
            
            # Return the Timeline
            return Timeline(timeline_dates)
            
        except (json.JSONDecodeError) as e: 
            traceback.print_exc()
            print(f'Error decoding JSON. Expected json from LLM but got {response_text}')
            raise e
        
        except (ClientError, Exception) as e:
            traceback.print_exc()
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            print(f"LLM Response: {response_text}")
            print(f"Formatted JSON: {timeline_json}")
            exit(1)
    