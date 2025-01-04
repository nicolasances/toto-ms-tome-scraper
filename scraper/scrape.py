from playwright.sync_api import sync_playwright

def scrape_blog(url: str) -> str:
    """Scrapes the provided blog. 
    This method extracts all the html of the blog and returns it.

    Args:
        url (str): The full URL of the blog

    Returns:
        str: the HTML content of the blog
    """
    
    # Initialize Playwright
    with sync_playwright() as p:
        
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the blog page
        page.goto(url, wait_until="networkidle")
        
        # Optionally wait for a specific element to load (e.g., content container)
        # page.wait_for_selector("div.blog-content")
        
        # Extract the content of the blog
        blog_content = page.content()  # Get the entire page HTML
        # blog_text = page.inner_text("page-body-div")  # Extract text from a specific element
        
        # Close the browser
        browser.close()
        
        return blog_content
        