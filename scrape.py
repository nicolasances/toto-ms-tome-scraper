from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_blog(url):
    # Initialize Playwright
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the blog page
        page.goto(url, wait_until="networkidle")
        
        # Optionally wait for a specific element to load (e.g., content container)
        page.wait_for_selector("p", timeout=10000)  # 10 seconds timeout
        
        # Extract the content of the blog
        blog_content = page.content()  # Get the entire page HTML
        
        # Close the browser
        browser.close()
        
        soup = BeautifulSoup(blog_content, "html.parser")
        
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
                
        # Print the sections array
        for section in sections:
            print('-----------------------------------')
            print(section["title"])
            print(section["content"])
            print("\n")

if __name__ == "__main__":
    # blog_url = "https://snails-shop-mta.craft.me/PaZe4KH5lo6NXF"  # Replace with your blog's URL
    blog_url = "https://snails-shop-mta.craft.me/RsmQFFdlfFLR0S"  # Replace with your blog's URL
    
    print("Starting")
    result = scrape_blog(blog_url)
    
    # with open('blog.txt', 'w') as file: 
    #     file.write(result["html"])
    # print("Blog Text:\n", result["html"])

