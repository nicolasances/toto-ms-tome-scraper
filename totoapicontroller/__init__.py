"""
Toto API Controller - Python framework for building microservices.

Provides:
- TotoMicroservice: Main orchestrator for microservice initialization and lifecycle
- TotoAPIController: FastAPI-based REST API framework
- TotoMessageBus: Message broker for event-driven architecture
- TotoControllerConfig: Base configuration class for secrets management
"""

# Core classes
from totoapicontroller.TotoMicroservice import (
    TotoMicroservice,
    TotoMicroserviceConfiguration,
    APIConfiguration,
    MessageBusConfiguration,
    MessageBusHandlerConfig,
    MessageBusTopicConfig,
)

from totoapicontroller.api.TotoAPIController import (
    TotoAPIController,
    HTTPMethod,
)

from totoapicontroller.api.APIControllerProps import APIControllerProps
from totoapicontroller.api.APIControllerOptions import APIControllerOptions

from totoapicontroller.evt.TotoMessageBus import (
    TotoMessageBus,
    MessageHandlerRegistration,
)

from totoapicontroller.evt.MessageBusConfig import (
    MessageBusConfiguration as MessageBusConfigType,
    TopicIdentifier,
    MessageHandlerRegistrationOptions,
)

from totoapicontroller.evt.TotoMessage import TotoMessage
from totoapicontroller.evt.TotoMessageHandler import (
    TotoMessageHandler,
    ProcessingResponse,
    ProcessingStatus,
)
from totoapicontroller.evt.MessageDestination import MessageDestination

from totoapicontroller.model.TotoConfig import TotoControllerConfig
from totoapicontroller.model.TotoEnvironment import (
    TotoEnvironment,
    AWSConfiguration,
    GCPConfiguration,
    AzureConfiguration,
)
from totoapicontroller.model.Hyperscaler import Hyperscaler
from totoapicontroller.model.PathOptions import PathOptions

# Logger
from totoapicontroller.TotoLogger import TotoLogger

# Utilities
from totoapicontroller.secrets.SecretsManager import SecretsManager

__all__ = [
    # Microservice
    "TotoMicroservice",
    "TotoMicroserviceConfiguration",
    "APIConfiguration",
    "MessageBusConfiguration",
    "MessageBusHandlerConfig",
    "MessageBusTopicConfig",
    # API Controller
    "TotoAPIController",
    "HTTPMethod",
    "APIControllerProps",
    "APIControllerOptions",
    # Message Bus
    "TotoMessageBus",
    "MessageHandlerRegistration",
    "TopicIdentifier",
    "MessageHandlerRegistrationOptions",
    # Messages
    "TotoMessage",
    "TotoMessageHandler",
    "ProcessingResponse",
    "ProcessingStatus",
    "MessageDestination",
    # Configuration
    "TotoControllerConfig",
    "TotoEnvironment",
    "AWSConfiguration",
    "GCPConfiguration",
    "AzureConfiguration",
    "Hyperscaler",
    "PathOptions",
    # Logger
    "TotoLogger",
    # Secrets
    "SecretsManager",
]
