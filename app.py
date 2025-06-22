from flask import Flask, request
from flask_cors import CORS

from dlg.scrape import extract_blog_content
from dlg.test.test_refresher import test_refresher
from dlg.test.test_pubsub import test_pubsub
from evt.ontopic import on_topic_event

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/', methods=['GET'])
def smoke():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.route('/blogs', methods=['POST'])
def post_blog_scraping_request(): 
    return extract_blog_content(request)

# -----------------------------------------------------------------------------------
# EVENTS
# -----------------------------------------------------------------------------------
@app.route('/events/topic', methods=['POST'])
def post_topic_event(): 
    return on_topic_event(request)

# -----------------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------------
@app.route('/test/refresher', methods=['POST'])
def test_refresher_generation(): 
    return test_refresher(request)

@app.route('/test/pubsub', methods=['POST'])
def test_pubsub_integration(): 
    return test_pubsub(request)


if __name__ == '__main__':
    app.run()