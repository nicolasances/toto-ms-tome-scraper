from flask import Flask, request
from flask_cors import CORS

from dlg.scrape import get_knowledge_from_blog

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/', methods=['GET'])
def smoke():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.route('/scrape', methods=['POST'])
def post_scrape(): 
    return get_knowledge_from_blog(request)

if __name__ == '__main__':
    app.run()