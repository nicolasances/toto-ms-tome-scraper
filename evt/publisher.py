import json
from datetime import datetime
from google.cloud import pubsub_v1

class TotoEventPublisher:
    
    def __init__(self, topic, exec_context):
        """
        :param topic: google.cloud.pubsub_v1.PublisherClient().topic_path(...)
        :param exec_context: An object with a 'logger' attribute
        """
        self.topic = topic
        self.exec_context = exec_context
        self.cid = exec_context.cid
        self.publisher = pubsub_v1.PublisherClient()

    def publishEvent(self, id: str, eventType: str, msg: str, data=None):
        
        logger = self.exec_context.logger

        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        message = json.dumps({
            "timestamp": timestamp,
            "cid": self.cid,
            "id": id,
            "type": eventType,
            "msg": msg,
            "data": data
        })

        logger.log(self.cid, f"Publishing the event [ {eventType} ] on topic [ {self.topic} ] for object with id [ {id} ]. The following message is to be published: [ {message} ]")

        try:
            self.publisher.publish(self.topic, data=message.encode('utf-8'))
            
            logger.log(self.cid, f"Successfully published the event [ {eventType} ]")
            
            return {"published": True}
        
        except Exception as e:
            logger.log(self.cid, f"Publishing the event [ {eventType} ] failed. The following message had to be published: [ {message} ]", "error")
            logger.log(self.cid, str(e), "error")
            print(e)
            return {"published": False}