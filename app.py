from flask import Flask, request
from flask_cors import CORS

from dlg.scrape import extract_blog_content

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/', methods=['GET'])
def smoke():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.route('/blogs', methods=['POST'])
def post_blog_scraping_request(): 
    return extract_blog_content(request)

if __name__ == '__main__':
    app.run()