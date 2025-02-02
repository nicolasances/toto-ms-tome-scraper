from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.blog import BlogContent
from model.timeline import Timeline
from util.naming import generate_section_code, generate_topic_code
from google.cloud import storage

class KnowledgeBaseStorage: 
    
    knowledge_base_folder: str = 'kb'
    
    def __init__(self, exec_context: ExecutionContext): 
        self.config = exec_context.config
        self.logger = exec_context.logger
        self.cid = exec_context.cid
        self.client = storage.Client()

    def store_blog_content(self, blog_content: BlogContent) -> str: 
        """Stores the blog content in the knowledge base
        
        Args:
            blog_content (BlogContent): The blog content to be stored, including its title and sections.
        Returns:
            str: The generated topic_code 
        """
        
        self.logger.log(self.cid, f'Storing Blog "{blog_content.title}" in the knowledge base')
        
        # 1. Get the Bucket
        bucket = self.client.get_bucket(self.config.get_tome_bucket_name())
        
        # 2. Generate the Topic Code 
        topic_code = generate_topic_code(blog_content.title)
        
        # 3. Store each section of the blog into its own file in the bucket
        for section in blog_content.sections: 
            
            self.logger.log(self.cid, f'Storing Section "{section.title}" in the knowledge base')
            
            # 3.1 Generate the Section Code
            section_code = generate_section_code(section.title)
            
            # 3.2 Generate the file path
            filepath = filepath = f'{self.knowledge_base_folder}/{topic_code}/{section_code}.txt'
            
            # 3.3 Get the blob
            blob = bucket.blob(filepath)
            
            # 3.4 Write the content
            self.logger.log(self.cid, f'Writing Knowledge Base file: {blob.name} to GCS bucket {bucket.name}')
            
            with blob.open('w') as file:
                file.write(section.content)
        
        return topic_code


        
        