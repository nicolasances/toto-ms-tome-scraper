"""
Message Handler base classes for processing messages.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
from totoapicontroller.evt.TotoMessage import TotoMessage


class ProcessingStatus(str, Enum):
    """Status of message processing."""
    SUCCESS = "success"
    FAILED = "failed"
    IGNORED = "ignored"


@dataclass
class ProcessingResponse:
    """
    Response from processing a message.
    
    Attributes:
        status: The processing status
        response_payload: The response payload (optional)
        error: Error message if processing failed (optional)
    """
    status: ProcessingStatus
    response_payload: Optional[Any] = None
    error: Optional[str] = None


class TotoMessageHandler(ABC):
    """
    Base class for message handlers.
    
    Subclasses must implement the get_handled_message_type() and process_message() methods.
    """
    
    @abstractmethod
    def get_handled_message_type(self) -> str:
        """
        Returns the message type this handler processes.
        
        Returns:
            The message type identifier
        """
        pass
    
    @abstractmethod
    async def process_message(self, message: TotoMessage) -> ProcessingResponse:
        """
        Processes a message.
        
        Args:
            message: The TotoMessage to process
            
        Returns:
            A ProcessingResponse indicating the result of processing
        """
        pass
