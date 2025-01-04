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
        
        paragraphs = soup.find_all("p")
        
        content = []
        
        for p in paragraphs: 
            content.append(p.get_text(strip=True))

        return content