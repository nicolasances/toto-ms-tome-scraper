from typing import List
from bs4 import BeautifulSoup

class BlobTextExtractor:
    
    def __init__(self, html_content: str): 
        self.html_content = html_content
        
    def get_text(self) -> List[str]: 
        """Retrieves all the text content of the blog. 
        This ONLY retrieves the <p> content. 
        It will not retrieve the headers, for example.

        Returns:
            List[str]: each text content of a <p>
        """
        
        soup = BeautifulSoup(self.html_content, "html.parser")
        
        # Extract the h1 tag
        h1 = soup.find("h1")
        
        blob_title = h1.get_text(strip=True) if h1 is not None else None
        
        # Find all tags that are either p or h4 
        tags = soup.find_all(["p", "h4"])
        
        # Go through each tag and whenever a h4 is found, create a list of all the p tags that follow it
        # This is to group the content of each section together
        # Each section must be an dict made of a "title" and a "content" key. The title is the h4 tag and the content is a list of p tags' content. 
        sections = []
        section = None
        for tag in tags:
            if tag.name == "h4":
                section = {"title": tag.get_text(strip=True), "content": []}
                sections.append(section)
            elif tag.name == "p" and section is not None:
                section["content"].append(tag.get_text(strip=True))
                
        return {
            "title": blob_title,    
            "sections": sections
        }
    
    