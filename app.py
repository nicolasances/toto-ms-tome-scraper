"""
Toto Tome Scraper - Microservice for scraping and processing tome content.

Uses TotoMicroservice framework for:
- Configuration management
- API controller with FastAPI
- Message bus for event handling

Run with: python app.py
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
from totoapicontroller.TotoMicroservice import APIEndpoint, determine_environment, MessageBusTopicConfig, MessageBusConfig

from dlg.scrape import extract_blog_content
from dlg.test.test_refresher import test_refresher
from dlg.test.test_pubsub import test_pubsub
from evt.ontopic import on_topic_event


def get_microservice_config() -> TotoMicroserviceConfiguration:
    """Create and return the microservice configuration."""
    return TotoMicroserviceConfiguration(
        service_name="toto-ms-tome-scraper",
        base_path="/tomescraper",
        environment=TotoEnvironment(
            hyperscaler=os.getenv("HYPERSCALER", "aws").lower(),
            hyperscaler_configuration=determine_environment()
        ),
        custom_config=TomeScraperConfig,
        api_configuration=APIConfiguration(
            api_endpoints=[
                APIEndpoint(method="POST", path="/blogs", delegate=extract_blog_content),
                APIEndpoint(method="POST", path="/events/topic", delegate=on_topic_event),
                APIEndpoint(method="POST", path="/test/refresher", delegate=test_refresher),
                APIEndpoint(method="POST", path="/test/pubsub", delegate=test_pubsub),
            ]
        ),
        message_bus_configuration=MessageBusConfig(
            topics=[
                MessageBusTopicConfig(logical_name="tometopics", secret="tome_topics_topic_name")
            ]
        ),
    )


async def main():
    """Main entry point for running the microservice."""
    microservice = await TotoMicroservice.init(get_microservice_config())
    port = int(os.getenv("PORT", "8080"))
    await microservice.start(port=port)


if __name__ == "__main__":
    asyncio.run(main())
