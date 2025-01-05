from playwright.sync_api import sync_playwright

def scrape_blog(url: str, timeout: int = 10000) -> str:
    """Scrapes the provided blog. 
    This method extracts all the html of the blog and returns it.
    This scraper is currently ONLY valid for Craft blogs.

    Args:
        url (str): The full URL of the blog

    Returns:
        str: the HTML content of the blog
    """
    
    # Initialize Playwright
    with sync_playwright() as p:
        
        # Launch a headless browser
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the blog page
        page.goto(url, wait_until="networkidle")
        
        # Wait for elements that are necessary for the blog to load
        # This is Craft blog specific
        page.wait_for_selector("p.sc-dnaUSb", timeout=timeout)  # 10 seconds timeout
        
        # Extract the content of the blog
        blog_content = page.content()  # Get the entire page HTML
        
        # Close the browser
        browser.close()
        
        return blog_content
        