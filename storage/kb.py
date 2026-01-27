from abc import ABC, abstractmethod
import os
from typing import List
from totoms.model.ExecutionContext import ExecutionContext
from model.blog import BlogContent


class StorageBlogStructure: 
    
    topic_code: str 
    section_codes: List[str]
    
    def __init__(self, topic_code: str, section_codes: List[str]): 
        self.topic_code = topic_code
        self.section_codes = section_codes


class KnowledgeBaseStorage(ABC):
    """Abstract interface for knowledge base storage implementations"""
    
    @abstractmethod
    def __init__(self, exec_context: ExecutionContext):
        """Initialize the storage with execution context
        
        Args:
            exec_context (ExecutionContext): The execution context containing config, logger, and correlation ID
        """
        pass
    
    @abstractmethod
    def store_blog_content(self, blog_content: BlogContent) -> StorageBlogStructure:
        """Stores the blog content in the knowledge base
        
        Args:
            blog_content (BlogContent): The blog content to be stored, including its title and sections.
        Returns:
            StorageBlogStructure: The storage structure containing topic_code and section_codes
        """
        pass
    
    @abstractmethod
    def delete_topic_content(self, topic_name: str):
        """Deletes all the stored files for the specified topic
        
        Args:
            topic_name (str): The name of the topic to delete.
        """
        pass


class KnowledgeBaseStorageFactory: 
    
    @staticmethod
    def get_storage(exec_context: ExecutionContext) -> KnowledgeBaseStorage:
        """Create a knowledge base storage instance based on the storage type
        
        Args:
            exec_context (ExecutionContext): The execution context
            
        Returns:
            KnowledgeBaseStorage: An instance of the requested storage type
            
        Raises:
            ValueError: If the storage type is not supported
        """
        hyperscaler = os.getenv("HYPERSCALER", "gcp").lower()

        if hyperscaler == "gcp":
            from storage.impl.gcs import GCSKnowledgeBaseStorage
            return GCSKnowledgeBaseStorage(exec_context)
        elif hyperscaler == "aws":
            from storage.impl.aws import S3KnowledgeBaseStorage
            return S3KnowledgeBaseStorage(exec_context)
        else:
            raise ValueError(f"Unsupported hyperscaler: {hyperscaler}")