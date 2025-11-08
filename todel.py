import json
import boto3

bedrock = boto3.client('bedrock-runtime', region_name="eu-central-1")

models = {
    "anthropic.claude-3.5-sonnet": {
        "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    },
    "anthropic.claude-3.7-sonnet": {
        "model_id": "eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
    },
    "anthropic.claude-4-sonnet": {
        "model_id": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
    }
}


try:

    prompt = "Hello"

    selected_model = "anthropic.claude-3.5-sonnet"
    model_info = models.get(selected_model, models["anthropic.claude-3.5-sonnet"])

    conversation = [
        {
            "role": "user", 
            "content": [{"text": prompt}]
        }
    ]

    response = bedrock.converse(
        modelId=model_info["model_id"], 
        messages=conversation, 
        inferenceConfig={
            "temperature": 0.3,
            "topP": 0.9,
            }
    )

    response_text = response['output']['message']['content'][0]['text']

    print(response_text)

except Exception as e:
    print(e)
