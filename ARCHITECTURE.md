# Toto API Controller - Python Implementation

This document describes the Python implementation of the Toto API Controller framework, which follows the TypeScript architecture from the `tome-ms-topics` project.

## Architecture Overview

The Toto API Controller is a framework for building microservices with the following components:

### 1. **TotoMicroservice** - Application Orchestrator
The main entry point for initializing and running a microservice.

**Key Features:**
- Singleton pattern for application-wide access
- Async initialization with dependency injection
- Coordinates configuration loading, API controller setup, and message bus initialization
- Manages the service lifecycle

**Usage:**
```python
from totoapicontroller import TotoMicroservice, TotoMicroserviceConfiguration, TotoEnvironment

config = TotoMicroserviceConfiguration(
    service_name="my-service",
    environment=TotoEnvironment(...),
    custom_config=MyCustomConfig,
    api_configuration=APIConfiguration(api_endpoints=[...]),
    message_bus_configuration=MessageBusConfiguration(...)
)

microservice = await TotoMicroservice.init(config)
await microservice.start(port=8080)
```

### 2. **TotoAPIController** - REST API Framework
Flask-based REST API controller with built-in validation and error handling.

**Key Features:**
- Path registration for HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Base path configuration for versioning
- File upload support
- Streaming responses
- Static content serving
- CORS handling
- Standard health check endpoints

**Usage:**
```python
from totoapicontroller import TotoAPIController, HTTPMethod, PathOptions

# Paths are registered via the microservice configuration
# Or directly:
api_controller.path(
    HTTPMethod.GET,
    "/users/{id}",
    handler_function,
    PathOptions(content_type="application/json")
)

api_controller.listen(port=8080)
```

### 3. **TotoMessageBus** - Event-Driven Architecture
Publish/Subscribe message broker supporting multiple hyperscalers.

**Key Features:**
- Support for AWS SNS, GCP Pub/Sub, Azure Service Bus
- Message handler registration for different message types
- Both PUSH (webhook) and PULL (polling) delivery models
- Topic name resolution (logical names → resource identifiers)
- Message routing to appropriate handlers
- Integration with API Controller for PUSH endpoints

**Usage:**
```python
from totoapicontroller import TotoMessageBus, TotoMessageHandler, ProcessingResponse, ProcessingStatus

# Create a message handler
class MyMessageHandler(TotoMessageHandler):
    def get_handled_message_type(self) -> str:
        return "user.created"
    
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        # Process the message
        return ProcessingResponse(
            status=ProcessingStatus.SUCCESS,
            response_payload={"processed": True}
        )

# Register the handler via MessageBusConfiguration
message_bus.register_message_handler(MyMessageHandler(config))

# Publish messages
await message_bus.publish_message(
    MessageDestination(topic="user-updates-topic"),
    TotoMessage(type="user.created", payload={"user_id": 123})
)
```

### 4. **TotoControllerConfig** - Configuration Management
Abstract base class for loading and managing service configuration.

**Key Features:**
- Lazy loading of secrets from cloud providers
- JWT key and audience management
- Database connection management (MongoDB)
- Extensible for service-specific configuration
- Properties for debugging and logging

**Implementation:**
```python
from totoapicontroller import TotoControllerConfig

class MyServiceConfig(TotoControllerConfig):
    def get_api_name(self) -> str:
        return "my-service"
    
    def get_expected_audience(self) -> str:
        return "my-service-audience"
    
    def get_mongo_secret_names(self) -> Optional[Dict[str, str]]:
        return {
            "user_secret_name": "mongo-user",
            "pwd_secret_name": "mongo-password"
        }
    
    @property
    def my_custom_config(self) -> str:
        # Custom configuration loading
        return self.secrets_manager.get_secret("my-custom-key")
```

## Design Patterns

### Singleton Pattern
`TotoMicroservice` uses a singleton pattern to ensure only one instance exists per application:
- `init()` creates the singleton
- `get_instance()` retrieves it
- Thread-safe initialization with async locks

### Dependency Injection
Configuration and dependencies are passed through constructors:
- APIControllerProps
- MessageBusConfiguration
- Custom configuration classes

### Handler Registration
Similar to TypeScript implementation:
- API endpoint handlers registered with path, method, and options
- Message handlers registered by message type
- Delegate pattern for flexible handler implementations

### Topic Resolution
Logical topic names are resolved to cloud provider resource identifiers:
- Configuration specifies logical name → secret mapping
- Secrets manager provides actual resource identifiers
- Allows environment-specific topic configuration

## Best Practices Applied

1. **Type Hints**: Full type annotations throughout for IDE support and type checking
2. **Docstrings**: Comprehensive docstrings in Google format
3. **Dataclasses**: Used for configuration objects with `@dataclass` decorator
4. **Abstract Base Classes**: ABC used for extensibility (TotoControllerConfig, TotoMessageHandler)
5. **Enums**: Used for HTTP methods and processing status
6. **Context Managers**: Proper resource management
7. **Async/Await**: Async operations for I/O and external service calls
8. **Module Organization**: Clear separation of concerns with subpackages
9. **Package Exports**: Organized `__init__.py` files for clean imports
10. **Error Handling**: Comprehensive error handling with meaningful messages

## File Structure

```
totoapicontroller/
├── __init__.py                    # Main package exports
├── TotoMicroservice.py            # Core orchestrator
├── TotoLogger.py                  # Logging utility
├── TotoDelegateDecorator.py      # Handler decorators
├── TotoTokenVerifier.py          # JWT token verification
├── api/
│   ├── __init__.py
│   ├── TotoAPIController.py      # Flask REST API
│   ├── APIControllerProps.py     # Configuration properties
│   └── APIControllerOptions.py   # Configuration options
├── evt/
│   ├── __init__.py
│   ├── TotoMessageBus.py         # Message broker
│   ├── TotoMessage.py            # Message model
│   ├── TotoMessageHandler.py     # Handler interface
│   ├── MessageBusConfig.py       # Configuration types
│   └── MessageDestination.py     # Destination model
├── model/
│   ├── __init__.py
│   ├── TotoConfig.py             # Base configuration
│   ├── TotoEnvironment.py        # Environment configuration
│   ├── Hyperscaler.py            # Hyperscaler enum
│   ├── PathOptions.py            # Path configuration
│   ├── UserContext.py            # User context
│   ├── ExecutionContext.py       # Execution context
│   └── ValidationResult.py       # Validation results
└── secrets/
    ├── __init__.py
    └── SecretsManager.py         # Secrets management
```

## Initialization Flow

1. **Configuration Phase**
   - Create `TotoMicroserviceConfiguration`
   - Specify service name, environment, custom config
   - Define API endpoints and message handlers

2. **Initialization Phase** (async)
   - Call `TotoMicroservice.init(config)`
   - Logger initialized with service name
   - SecretsManager created for credential management
   - Custom configuration loaded with secrets
   - Topic names resolved from secrets manager
   - APIController created with properties and options
   - MessageBus created and handlers registered
   - API endpoints registered with controllers

3. **Startup Phase**
   - Call `microservice.start(port)`
   - APIController initialized (registry registration, etc.)
   - Flask app starts listening on specified port
   - Message bus begins handling incoming messages

## Message Flow

### Publishing Messages
```
TotoMicroservice
  ├─ TotoMessageBus.publish_message()
  │  ├─ Validate destination
  │  ├─ Resolve topic name (logical → resource ID)
  │  └─ Delegate to hyperscaler implementation
  │     ├─ AWS SNS
  │     ├─ GCP Pub/Sub
  │     └─ Azure Service Bus
```

### Consuming Messages (PULL)
```
Queue Implementation
  ├─ Poll for messages
  ├─ MessageBus.on_pull_message_received()
  │  ├─ Convert to TotoMessage
  │  ├─ Find handler by message type
  │  └─ Handler.process_message()
```

### Consuming Messages (PUSH)
```
API Endpoint: POST /events
  ├─ MessageBus.on_push_message_received()
  │  ├─ Convert webhook to TotoMessage
  │  ├─ Find handler by message type
  │  └─ Handler.process_message()
```

## Extension Points

Services extend the framework by:

1. **Custom Configuration**
   ```python
   class MyServiceConfig(TotoControllerConfig):
       def get_api_name(self) -> str:
           return "my-service"
   ```

2. **Message Handlers**
   ```python
   class MyMessageHandler(TotoMessageHandler):
       def get_handled_message_type(self) -> str:
           return "my.message.type"
       
       async def process_message(self, message):
           # Handle message
   ```

3. **API Delegates**
   - Classes that handle specific API endpoints
   - Registered via APIConfiguration

## Comparison with TypeScript

| Feature | TypeScript | Python |
|---------|-----------|--------|
| Singleton | Manual instance tracking | Asyncio-aware singleton |
| Configuration | Constructor injection | Dataclass + abstract class |
| Async | Native Promise/async-await | asyncio support |
| Message Bus | SNS/GCP/Azure impls | Stub with impl framework |
| API Framework | Express.js | Flask |
| Validation | Custom validator | Extensible framework |
| Type Safety | TypeScript types | Type hints + dataclasses |

## Testing Considerations

- Mock hyperscaler implementations
- Use `TotoMicroserviceConfiguration` for test setup
- Stub message handlers for testing message flow
- Mock SecretsManager for credential testing
