import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dlg.scrape import extract_blog_content
from dlg.test.test_refresher import test_refresher
from dlg.test.test_pubsub import test_pubsub
from evt.ontopic import on_topic_event

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
def health_check():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.get('/')
def smoke_base():
    return {"api": "toto-ms-tome-scraper", "running": True}

@app.get('/tomescraper/smoke')
def smoke():
    return {"api": "toto-ms-tome-scraper", "running": True, "hyperscaler": os.getenv("HYPERSCALER", "not-set"), "env": os.getenv("ENVIRONMENT", "not-set")}

@app.post('/tomescraper/blogs')
async def post_blog_scraping_request(request): 
    return await extract_blog_content(request)

# -----------------------------------------------------------------------------------
# EVENTS
# -----------------------------------------------------------------------------------
@app.post('/tomescraper/events/topic')
async def post_topic_event(request): 
    return await on_topic_event(request)

# -----------------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------------
@app.post('/tomescraper/test/refresher')
async def test_refresher_generation(request): 
    return await test_refresher(request)

@app.post('/tomescraper/test/pubsub')
async def test_pubsub_integration(request): 
    return await test_pubsub(request)