# Quick Start Guide - Toto API Controller

## Installation

Ensure the `totoapicontroller` package is in your Python path.

```bash
pip install -r requirements.txt
```

## Basic Service Setup

### Step 1: Create a Custom Configuration Class

```python
# my_service_config.py
from totoapicontroller import TotoControllerConfig
from typing import Optional, Dict

class MyServiceConfig(TotoControllerConfig):
    """Custom configuration for my-service."""
    
    def get_api_name(self) -> str:
        """Return the API name."""
        return "my-service"
    
    def get_expected_audience(self) -> str:
        """Return the expected JWT audience."""
        return "my-service:prod"
    
    def get_mongo_secret_names(self) -> Optional[Dict[str, str]]:
        """Return MongoDB secret names if your service uses MongoDB."""
        return {
            "user_secret_name": "mongo-user",
            "pwd_secret_name": "mongo-password"
        }
    
    # Add any custom configuration properties here
    @property
    def custom_api_key(self) -> str:
        """Example of custom configuration."""
        return self.secrets_manager.get_secret("custom-api-key")
```

### Step 2: Create Message Handlers (Optional)

```python
# handlers.py
from totoapicontroller import TotoMessageHandler, TotoMessage, ProcessingResponse, ProcessingStatus

class UserCreatedHandler(TotoMessageHandler):
    """Handles user.created messages."""
    
    def get_handled_message_type(self) -> str:
        return "user.created"
    
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        user_id = message.payload.get("user_id")
        print(f"User created: {user_id}")
        
        # Process the user creation...
        
        return ProcessingResponse(
            status=ProcessingStatus.SUCCESS,
            response_payload={"user_id": user_id, "processed": True}
        )

class OrderProcessedHandler(TotoMessageHandler):
    """Handles order.processed messages."""
    
    def get_handled_message_type(self) -> str:
        return "order.processed"
    
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        order_id = message.payload.get("order_id")
        print(f"Order processed: {order_id}")
        
        # Process the order...
        
        return ProcessingResponse(status=ProcessingStatus.SUCCESS)
```

### Step 3: Create API Endpoint Handlers (Delegates)

```python
# delegates.py
class GetUsersDelegate:
    """Handler for GET /users endpoint."""
    
    def __init__(self, message_bus, config):
        self.message_bus = message_bus
        self.config = config
    
    def handle(self, request):
        """Handle the request."""
        # Return user data
        return {"users": []}

class CreateUserDelegate:
    """Handler for POST /users endpoint."""
    
    def __init__(self, message_bus, config):
        self.message_bus = message_bus
        self.config = config
    
    async def handle(self, request):
        """Handle the request."""
        user_data = request.json
        
        # Publish an event
        await self.message_bus.publish_message(
            MessageDestination(topic="user-updates-topic"),
            TotoMessage(
                type="user.created",
                payload=user_data
            )
        )
        
        return {"user_id": 123, "created": True}
```

### Step 4: Initialize and Run the Service

```python
# main.py
import asyncio
from totoapicontroller import (
    TotoMicroservice,
    TotoMicroserviceConfiguration,
    TotoEnvironment,
    AWSConfiguration,
    APIConfiguration,
    MessageBusConfiguration,
    MessageBusTopicConfig,
    MessageBusHandlerConfig,
)
from my_service_config import MyServiceConfig
from handlers import UserCreatedHandler, OrderProcessedHandler
from delegates import GetUsersDelegate, CreateUserDelegate

async def main():
    # Configure the environment
    environment = TotoEnvironment(
        hyperscaler="aws",
        hyperscaler_configuration=AWSConfiguration(
            region="us-east-1",
            environment="prod"
        )
    )
    
    # Configure message bus topics
    message_bus_config = MessageBusConfiguration(
        topics=[
            MessageBusTopicConfig("user-updates-topic", "user-topic-arn-secret"),
            MessageBusTopicConfig("order-updates-topic", "order-topic-arn-secret"),
        ],
        message_handlers=[
            MessageBusHandlerConfig(UserCreatedHandler),
            MessageBusHandlerConfig(OrderProcessedHandler),
        ]
    )
    
    # Configure API endpoints
    api_config = APIConfiguration(
        api_endpoints=[
            # GET /api/v1/users
            {
                "method": "GET",
                "path": "/users",
                "delegate": GetUsersDelegate
            },
            # POST /api/v1/users
            {
                "method": "POST",
                "path": "/users",
                "delegate": CreateUserDelegate
            },
        ]
    )
    
    # Create microservice configuration
    config = TotoMicroserviceConfiguration(
        service_name="my-service",
        base_path="/api/v1",
        environment=environment,
        custom_config=MyServiceConfig,
        api_configuration=api_config,
        message_bus_configuration=message_bus_config
    )
    
    # Initialize the microservice
    microservice = await TotoMicroservice.init(config)
    
    # Start the service
    await microservice.start(port=8080)

if __name__ == "__main__":
    asyncio.run(main())
```

## Common Patterns

### Publishing Messages

```python
from totoapicontroller import TotoMessage, MessageDestination

# In a delegate or handler
async def publish_event():
    await self.message_bus.publish_message(
        destination=MessageDestination(topic="my-topic"),
        message=TotoMessage(
            type="my.event.type",
            payload={"key": "value"},
            correlation_id="request-123"
        )
    )
```

### Accessing Configuration

```python
class MyDelegate:
    def __init__(self, message_bus, config):
        self.config = config
    
    def handle(self):
        api_name = self.config.get_api_name()
        jwt_key = self.config.jwt_key
        mongo_host = self.config.mongo_host
        custom_value = self.config.custom_api_key
```

### Excluding Paths from Authentication

```python
class MyServiceConfig(TotoControllerConfig):
    def is_path_excluded(self, path: str) -> bool:
        excluded_paths = ["/", "/health", "/smoke", "/public/*"]
        return any(path.startswith(p.rstrip("*")) for p in excluded_paths)
```

### Handling Errors

```python
class MyHandler(TotoMessageHandler):
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        try:
            # Process the message
            result = await self.process(message.payload)
            return ProcessingResponse(
                status=ProcessingStatus.SUCCESS,
                response_payload=result
            )
        except Exception as e:
            return ProcessingResponse(
                status=ProcessingStatus.FAILED,
                error=str(e)
            )
```

## Troubleshooting

### Configuration Not Loaded
```python
# Make sure to await the load() method
config = MyServiceConfig(environment)
await config.load()
```

### Message Handler Not Receiving Messages
```python
# Ensure handler type matches message type exactly
class MyHandler(TotoMessageHandler):
    def get_handled_message_type(self) -> str:
        return "user.created"  # Must match published message type

# When publishing
TotoMessage(type="user.created", payload={...})  # Must match exactly
```

### Port Already in Use
```python
# Specify a different port
await microservice.start(port=8081)
```

## Environment Variables

Configure these via your cloud provider's secrets manager:

- `jwt-signing-key` - JWT signing key for token creation
- `toto-expected-audience` - Expected audience for JWT validation
- `toto-registry-endpoint` - Toto Registry endpoint
- `mongo-host` - MongoDB host (if using MongoDB)
- `mongo-user` - MongoDB username (if using MongoDB)
- `mongo-password` - MongoDB password (if using MongoDB)
- Topic ARN/names as configured in `MessageBusTopicConfig`

## Testing

### Mock Message Bus for Testing

```python
class MockMessageBus:
    async def publish_message(self, destination, message):
        print(f"Mock: Publishing {message.type} to {destination.topic}")

# In your test
config = MyServiceConfig(environment)
mock_bus = MockMessageBus()
delegate = MyDelegate(mock_bus, config)
result = delegate.handle()
```

### Test Handlers

```python
@pytest.mark.asyncio
async def test_user_handler():
    handler = UserCreatedHandler()
    message = TotoMessage(
        type="user.created",
        payload={"user_id": 123}
    )
    result = await handler.process_message(message)
    assert result.status == ProcessingStatus.SUCCESS
```

## Performance Considerations

1. **Connection Pooling** - MongoDB and cloud service clients should use connection pools
2. **Async Operations** - Always use async/await for I/O operations
3. **Message Batching** - Consider batching messages for high-throughput services
4. **Caching** - Cache configuration properties to avoid repeated secret lookups

## Further Reading

See `ARCHITECTURE.md` for detailed architecture documentation.
