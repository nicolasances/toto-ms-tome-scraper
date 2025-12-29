"""
TotoMessage class for representing messages in the message bus.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TotoMessage:
    """
    Represents a message in the Toto message bus.
    
    Attributes:
        type: The message type identifier
        payload: The message payload (can be any serializable data)
        correlation_id: Correlation ID for tracking (optional)
        timestamp: Message timestamp (optional)
        metadata: Additional metadata (optional)
    """
    type: str
    payload: Any
    correlation_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
