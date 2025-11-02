from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.blog import BlogContent
from util.naming import generate_section_code, generate_topic_code
from storage.kb import KnowledgeBaseStorage, StorageBlogStructure
from google.cloud import storage


class GCSKnowledgeBaseStorage(KnowledgeBaseStorage): 
    
    knowledge_base_folder: str = 'kb'
    
    def __init__(self, exec_context: ExecutionContext): 
        self.config = exec_context.config
        self.logger = exec_context.logger
        self.cid = exec_context.cid
        self.client = storage.Client()

    def store_blog_content(self, blog_content: BlogContent) -> StorageBlogStructure: 
        """Stores the blog content in the knowledge base
        
        Args:
            blog_content (BlogContent): The blog content to be stored, including its title and sections.
        Returns:
            str: The generated topic_code 
        """
        
        self.logger.log(self.cid, f'Storing Blog "{blog_content.title}" in the knowledge base. Storing {len(blog_content.sections)} sections.')
        
        # 1. Get the Bucket
        bucket = self.client.get_bucket(self.config.get_tome_bucket_name())
        
        # 2. Generate the Topic Code 
        topic_code = generate_topic_code(blog_content.title)
        
        # 3. Delete all files in the topic folder if it exists
        blobs = bucket.list_blobs(prefix=f'{self.knowledge_base_folder}/{topic_code}/')
        
        for blob in blobs:
            self.logger.log(self.cid, f'Deleting Knowledge Base file: {blob.name} from GCS bucket {bucket.name}')
            blob.delete()

        # 4. Store each section of the blog into its own file in the bucket
        section_codes = []
        for index, section in enumerate(blog_content.sections): 
            
            self.logger.log(self.cid, f'Storing Section "{section.title}" in the knowledge base')
            
            # 4.1 Generate the Section Code
            section_code = generate_section_code(section.title)
            section_codes.append(section_code)
            
            # 4.2 Generate the file path
            filepath = filepath = f'{self.knowledge_base_folder}/{topic_code}/{index}-{section_code}.txt'
            
            # 4.3 Get the blob
            blob = bucket.blob(filepath)
            
            # 4.4 Write the content
            self.logger.log(self.cid, f'Writing Knowledge Base file: {blob.name} to GCS bucket {bucket.name}')
            
            with blob.open('w') as file:
                file.write(section.content)
        
        return StorageBlogStructure(topic_code, section_codes)
    
    def delete_topic_content(self, topic_name: str): 
        """Deletes all the GCS stored files for the specified topic
        Args:
            topic_name (str): The name of the topic to delete.
        """
        self.logger.log(self.cid, f'Deleting topic "{topic_name}" from the knowledge base')
        
        # 1. Get the Bucket
        bucket = self.client.get_bucket(self.config.get_tome_bucket_name())
        
        # 2. Generate the Topic Code 
        topic_code = generate_topic_code(topic_name)
        
        # 3. Delete all the files in the topic folder
        blobs = bucket.list_blobs(prefix=f'{self.knowledge_base_folder}/{topic_code}/')
        for blob in blobs:
            self.logger.log(self.cid, f'Deleting Knowledge Base file: {blob.name} from GCS bucket {bucket.name}')
            blob.delete()
            
        self.logger.log(self.cid, f"Deleted all files for topic {topic_name}" )
        
        