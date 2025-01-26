"""
Error recovery utilities for PS SimC Parser
"""
import logging
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

class ErrorRecovery:
    """Handle error recovery and fallback strategies"""
    
    def __init__(self):
        self.error_count = 0
        self.warnings = []
        self.fallbacks: Dict[str, Any] = {}
        
    def handle_error(self, error: Exception, context: Optional[Dict] = None) -> None:
        """Handle an error and log it"""
        self.error_count += 1
        logger.error(f"Error occurred: {str(error)}", exc_info=True)
        if context:
            logger.error(f"Error context: {context}")
            
    def add_warning(self, message: str) -> None:
        """Add a warning message"""
        self.warnings.append(message)
        logger.warning(message)
        
    def register_fallback(self, key: str, value: Any) -> None:
        """Register a fallback value for a key"""
        self.fallbacks[key] = value
        logger.debug(f"Registered fallback for {key}: {value}")
        
    def get_fallback(self, key: str) -> Optional[Any]:
        """Get a fallback value for a key"""
        return self.fallbacks.get(key)
        
    def reset(self) -> None:
        """Reset error tracking"""
        self.error_count = 0
        self.warnings.clear()
        self.fallbacks.clear()

recovery = ErrorRecovery()
