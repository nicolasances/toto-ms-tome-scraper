from dataclasses import dataclass
from typing import List

from util.naming import generate_section_code, generate_topic_code

@dataclass
class BlogSection: 
    
    title: str 
    content: str
    
    def __init__(self, title: str, content: str): 
        
        self.title = title
        self.content = content

@dataclass
class BlogContent: 
    
    title: str 
    sections: List[BlogSection]
    
    def __init__(self, title: str, sections: List[BlogSection]): 
        
        self.title = title
        self.sections = sections
        
class TopicSection: 
    
    title: str 
    code: str 
    
    def __init__(self, blog_section: BlogSection): 
        
        self.title = blog_section.title
        self.code = generate_section_code(blog_section.title)
    
class Topic: 
    
    title: str 
    code: str 
    sections: List[TopicSection]
    
    def __init__(self, blog_content: BlogContent):  
        
        self.title = blog_content.title
        self.code = generate_topic_code(blog_content.title)
        self.sections = [TopicSection(blog_section) for blog_section in blog_content.sections]
        
        
    def to_bson(self): 
        return {
            "title": self.title, 
            "code": self.code, 
            "sections": [section.__dict__ for section in self.sections]
        }