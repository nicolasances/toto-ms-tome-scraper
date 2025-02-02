
from model.blog import BlogContent


def merge_sections(blog_content: BlogContent) -> str: 
    """Merges all the sections to create a long corpus of text. 

    Args:
        blog_content (BlogContent): the scraped content of the blog

    Returns:
        str: the merged sections (corpus)
    """
    sections_content = []
    
    for section in blog_content.sections: 
        sections_content.append(section.content)
    
    return ' '.join(sections_content)
    