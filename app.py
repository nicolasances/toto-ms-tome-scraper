import os
from flask import Flask, request
from flask_cors import CORS

from dlg.scrape import extract_blog_content
from dlg.test.test_refresher import test_refresher
from dlg.test.test_pubsub import test_pubsub
from evt.ontopic import on_topic_event

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/health', methods=['GET'])
def health_check():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.route('/', methods=['GET'])
def smoke_base():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.route('/tomescraper/smoke', methods=['GET'])
def smoke():
    return {"api": "toto-ms-tome-scraper", "running": True, "hyperscaler": os.getenv("HYPERSCALER", "not-set"), "env": os.getenv("ENVIRONMENT", "not-set")}

@app.route('/tomescraper/blogs', methods=['POST'])
def post_blog_scraping_request(): 
    return extract_blog_content(request)

# -----------------------------------------------------------------------------------
# EVENTS
# -----------------------------------------------------------------------------------
@app.route('/tomescraper/events/topic', methods=['POST'])
def post_topic_event(): 
    return on_topic_event(request)

# -----------------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------------
@app.route('/tomescraper/test/refresher', methods=['POST'])
def test_refresher_generation(): 
    return test_refresher(request)

@app.route('/tomescraper/test/pubsub', methods=['POST'])
def test_pubsub_integration(): 
    return test_pubsub(request)


if __name__ == '__main__':
    app.run()