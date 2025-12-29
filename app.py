"""
Toto Tome Scraper - Microservice for scraping and processing tome content.

Uses TotoMicroservice framework for:
- Configuration management
- API controller with FastAPI
- Message bus for event handling
"""
import asyncio
import os
from config.config import TomeScraperConfig
from totoapicontroller import (
    TotoMicroservice,
    TotoMicroserviceConfiguration,
    TotoEnvironment,
    APIConfiguration,
)
from totoapicontroller.TotoMicroservice import APIEndpoint, determine_environment

from dlg.scrape import extract_blog_content
from dlg.test.test_refresher import test_refresher
from dlg.test.test_pubsub import test_pubsub
from evt.ontopic import on_topic_event

async def main():
    """Main entry point."""
    microservice = await TotoMicroservice.init( TotoMicroserviceConfiguration(
        service_name="toto-ms-tome-scraper",
        base_path="/tomescraper",
        environment=TotoEnvironment(
            hyperscaler=os.getenv("HYPERSCALER", "aws").lower(),
            hyperscaler_configuration=determine_environment()
        ),
        custom_config=TomeScraperConfig,
        api_configuration=APIConfiguration(
            api_endpoints=[
                APIEndpoint(method="POST", path="/tomescraper/blogs", delegate=extract_blog_content),
                APIEndpoint(method="POST", path="/tomescraper/events/topic", delegate=on_topic_event),
                APIEndpoint(method="POST", path="/tomescraper/test/refresher", delegate=test_refresher),
                APIEndpoint(method="POST", path="/tomescraper/test/pubsub", delegate=test_pubsub),
            ]
        ),
        message_bus_configuration=None,  # Configure if needed for message handling
    ))
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", "8080"))
    
    # Start the service
    await microservice.start(port=port)


if __name__ == "__main__":
    asyncio.run(main())
