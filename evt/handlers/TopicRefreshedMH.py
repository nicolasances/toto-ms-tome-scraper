
from dlg.scrape import scrape_and_store_blog
from totoapicontroller.evt.TotoMessage import TotoMessage
from totoapicontroller.evt.TotoMessageBus import ProcessingResponse, ProcessingStatus
from totoapicontroller.evt.TotoMessageHandler import TotoMessageHandler
from totoapicontroller.model.ExecutionContext import ExecutionContext

class TopicRefreshedEventHandler(TotoMessageHandler): 
    
    def get_handled_message_type(self) -> str:
        return "topicRefreshed"
    
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        # Implement the logic to handle the topic refreshed event
        self.logger.log(message.cid, f"Processing TopicRefreshed event: {message.msg}")
        
        blog_url = message.data.get('blogURL')
        topic_name = message.data.get('name')
        topic_id = message.id
        user = message.data.get('user')
        
        exec_context = ExecutionContext(
            logger=self.logger,
            cid=message.cid, 
            config=self.config, 
            message_bus=self.message_bus,
            environment=self.environment
        )
        
        # Start the scraping process
        await scrape_and_store_blog(blog_url, topic_name, topic_id, user, exec_context)
        
        # For demonstration, we just log the message and return success
        return ProcessingResponse(status=ProcessingStatus.SUCCESS)