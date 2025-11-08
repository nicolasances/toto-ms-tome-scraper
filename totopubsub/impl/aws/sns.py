import boto3
import json
from totopubsub.pubsub import PubSub


class SNS(PubSub):
    
    def __init__(self):
        self.sns_client = boto3.client('sns')
        self.sts_client = boto3.client('sts')
    
    def publish_message(self, topic_name: str, message: dict):
        """
        Publish a message to an SNS topic.
        
        Args:
            topic_name: The name of the SNS topic (will be used to construct ARN or can be full ARN)
            message: Dictionary containing the message data
        """
        try:
            # If topic_name is not an ARN, construct it
            if not topic_name.startswith('arn:aws:sns:'):

                # Get AWS account ID and region from STS
                account_id = self.sts_client.get_caller_identity()['Account']
                
                region = self.sns_client.meta.region_name

                topic_arn = f"arn:aws:sns:{region}:{account_id}:{topic_name}"

            else:
                topic_arn = topic_name
            
            # Publish the message
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=json.dumps(message),
                MessageAttributes={
                    'ContentType': {
                        'DataType': 'String',
                        'StringValue': 'application/json'
                    }
                }
            )
            
            return response['MessageId']
            
        except Exception as e:
            raise Exception(f"Failed to publish message to SNS topic {topic_name}: {str(e)}")
