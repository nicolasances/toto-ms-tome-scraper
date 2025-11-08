

from abc import ABC, abstractmethod
import os
from typing import Dict

from totopubsub.model import TotoMessage



class PubSub(ABC):
    
    @abstractmethod
    def publish_message(self, topic_name: str, message: TotoMessage) -> Dict:
        """
        Publish a message to the specified topic.
        
        Args:
            topic_name: The name of the topic to publish to
            message: The TotoMessage to publish
            
        Returns:
            str: The message ID of the published message
            
        Raises:
            Exception: If publishing fails
        """
        pass
    
class PubSubFactory:

    @staticmethod
    def create_pubsub(exec_context=None):
        """
        Create a PubSub instance based on the HYPERSCALER environment variable.
        
        Args:
            exec_context: Required for GCP implementation
            
        Returns:
            PubSub: An instance of the appropriate PubSub implementation
        """
        # Import here to avoid circular imports
        from totopubsub.impl.aws.sns import SNS
        from totopubsub.impl.gcp.gcppubsub import GCPPubSub
        
        # 1. Get the environment 
        hyperscaler: str = exec_context.config.hyperscaler
        region: str = exec_context.config.region

        # 2. Create the PubSub according to the hyperscaler
        if hyperscaler == 'aws':
            return SNS(region, exec_context)
        elif hyperscaler == 'gcp':
            return GCPPubSub(exec_context)

        raise Exception(f"PubSub for hyperscaler {hyperscaler} is not implemented yet.")
