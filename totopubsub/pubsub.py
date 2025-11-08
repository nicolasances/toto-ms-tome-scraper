
from abc import ABC, abstractmethod
import os

from totopubsub.impl.aws.sns import SNS

class PubSub(ABC): 
    
    @abstractmethod
    def publish_message(self, topic_name: str, message: dict):
        pass


class PubSubFactory:

    @staticmethod
    def create_pubsub():

        # 1. Get the environment 
        hyperscaler: str = os.getenv('HYPERSCALER') if os.getenv('HYPERSCALER') else 'gcp'

        # 2. Create the PubSub according to the hyperscaler
        if hyperscaler == 'aws':
            return SNS()

        raise Exception(f"PubSub for hyperscaler {hyperscaler} is not implemented yet.")
