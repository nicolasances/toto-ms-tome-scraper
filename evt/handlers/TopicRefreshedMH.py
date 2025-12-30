
from totoapicontroller.evt.TotoMessage import TotoMessage
from totoapicontroller.evt.TotoMessageBus import ProcessingResponse, ProcessingStatus
from totoapicontroller.evt.TotoMessageHandler import TotoMessageHandler


class TopicRefreshedEventHandler(TotoMessageHandler): 
    
    def get_handled_message_type(self) -> str:
        return "topicRefreshed"
    
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        # Implement the logic to handle the topic refreshed event
        self.logger.log(message.cid, f"Processing TopicRefreshed event: {message.msg}")
        
        # For demonstration, we just log the message and return success
        return ProcessingResponse(status=ProcessingStatus.SUCCESS)