from totoapicontroller.model.ExecutionContext import ExecutionContext

from model.blog import BlogContent
from util.naming import generate_section_code, generate_topic_code
from storage.kb import KnowledgeBaseStorage, StorageBlogStructure
import boto3
from botocore.exceptions import ClientError
import os


class S3KnowledgeBaseStorage(KnowledgeBaseStorage):
    
    knowledge_base_folder: str = 'kb'
    
    def __init__(self, exec_context: ExecutionContext): 
        self.config = exec_context.config
        self.logger = exec_context.logger
        self.cid = exec_context.cid
        self.client = boto3.client('s3')

    def store_blog_content(self, blog_content: BlogContent) -> StorageBlogStructure: 
        """Stores the blog content in the knowledge base
        
        Args:
            blog_content (BlogContent): The blog content to be stored, including its title and sections.
        Returns:
            StorageBlogStructure: The generated topic_code and section_codes
        """
        
        self.logger.log(self.cid, f'Storing Blog "{blog_content.title}" in the knowledge base. Storing {len(blog_content.sections)} sections.')
        
        # 1. Get the Bucket name
        bucket_name = self._get_tome_bucket_name()
        
        # 2. Generate the Topic Code 
        topic_code = generate_topic_code(blog_content.title)
        
        # 3. Delete all files in the topic folder if it exists
        self._delete_objects_with_prefix(bucket_name, f'{self.knowledge_base_folder}/{topic_code}/')

        # 4. Store each section of the blog into its own file in the bucket
        section_codes = []
        for index, section in enumerate(blog_content.sections): 
            
            self.logger.log(self.cid, f'Storing Section "{section.title}" in the knowledge base')
            
            # 4.1 Generate the Section Code
            section_code = generate_section_code(section.title)
            section_codes.append(section_code)
            
            # 4.2 Generate the file path
            filepath = f'{self.knowledge_base_folder}/{topic_code}/{index}-{section_code}.txt'
            
            # 4.3 Write the content to S3
            self.logger.log(self.cid, f'Writing Knowledge Base file: {filepath} to S3 bucket {bucket_name}')
            
            self.client.put_object(
                Bucket=bucket_name,
                Key=filepath,
                Body=section.content,
                ContentType='text/plain'
            )
        
        return StorageBlogStructure(topic_code, section_codes)
    
    def delete_topic_content(self, topic_name: str): 
        """Deletes all the S3 stored files for the specified topic
        Args:
            topic_name (str): The name of the topic to delete.
        """
        self.logger.log(self.cid, f'Deleting topic "{topic_name}" from the knowledge base')
        
        # 1. Get the Bucket name
        bucket_name = self._get_tome_bucket_name()
        
        # 2. Generate the Topic Code 
        topic_code = generate_topic_code(topic_name)
        
        # 3. Delete all the files in the topic folder
        self._delete_objects_with_prefix(bucket_name, f'{self.knowledge_base_folder}/{topic_code}/')
            
        self.logger.log(self.cid, f"Deleted all files for topic {topic_name}")
    
    def _get_tome_bucket_name(self) -> str:
        """Get the S3 bucket name for tome data
        
        Returns:
            str: The S3 bucket name
        """
        toto_env = os.getenv('ENVIRONMENT', 'dev')
        
        bucket_name = f'toto-tome-bucket-{toto_env}'
        
        return bucket_name
    
    def _delete_objects_with_prefix(self, bucket_name: str, prefix: str):
        """Delete all objects in S3 bucket with the given prefix
        
        Args:
            bucket_name (str): The S3 bucket name
            prefix (str): The prefix to match objects for deletion
        """
        try:
            # List objects with the prefix
            response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            
            if 'Contents' in response:
                # Prepare objects for deletion
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
                
                if objects_to_delete:
                    # Delete objects in batch
                    self.logger.log(self.cid, f'Deleting {len(objects_to_delete)} Knowledge Base files from S3 bucket {bucket_name}')
                    
                    delete_response = self.client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': objects_to_delete}
                    )
                    
                    # Log individual deletions if needed
                    if 'Deleted' in delete_response:
                        for deleted_obj in delete_response['Deleted']:
                            self.logger.log(self.cid, f'Deleted Knowledge Base file: {deleted_obj["Key"]} from S3 bucket {bucket_name}')
                    
                    # Log any errors
                    if 'Errors' in delete_response:
                        for error in delete_response['Errors']:
                            self.logger.log(self.cid, f'Error deleting {error["Key"]}: {error["Message"]}')
            else:
                self.logger.log(self.cid, f'No files found with prefix {prefix} in bucket {bucket_name}')
                
        except ClientError as e:
            self.logger.log(self.cid, f'Error listing/deleting objects with prefix {prefix}: {e}')
            raise
