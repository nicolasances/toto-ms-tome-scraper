from dataclasses import dataclass
from typing import List

from util.naming import generate_section_code, generate_topic_code

@dataclass
class BlogSection: 
    
    title: str 
    content: str
    order: int
    
    def __init__(self, title: str, content: str, order: int): 
        
        self.title = title
        self.content = content
        self.order = order

@dataclass
class BlogContent: 
    
    title: str 
    sections: List[BlogSection]
    
    def __init__(self, title: str, sections: List[BlogSection]): 
        
        self.title = title
        self.sections = sections
        
class TopicSection: 
    
    order: int
    title: str 
    code: str 
    length: int
    
    def __init__(self, blog_section: BlogSection): 
        
        self.title = blog_section.title
        self.code = generate_section_code(blog_section.title)
        self.order = blog_section.order
        self.length = len(blog_section.content)
    
class Topic: 
    
    title: str 
    code: str 
    sections: List[TopicSection]
    blog_url: str 
    blog_type: str
    
    def __init__(self, blog_content: BlogContent, blog_url: str, blog_type: str):  
        
        self.title = blog_content.title
        self.code = generate_topic_code(blog_content.title)
        self.sections = [TopicSection(blog_section) for blog_section in blog_content.sections]
        self.blog_url = blog_url
        self.blog_type = blog_type
        
        
    def to_bson(self): 
        return {
            "title": self.title, 
            "code": self.code, 
            "blog_url": self.blog_url,
            "blog_type": self.blog_type,
            "sections": [section.__dict__ for section in self.sections]
        }