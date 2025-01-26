"""
Performance monitoring utilities for PS SimC Parser
"""
import time
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor performance of parser operations"""
    
    def __init__(self):
        self.operations: Dict[str, float] = {}
        self.start_times: Dict[str, float] = {}
        
    def start_operation(self, name: str) -> None:
        """Start timing an operation"""
        self.start_times[name] = time.time()
        logger.debug(f"Starting operation: {name}")
        
    def end_operation(self, name: str) -> Optional[float]:
        """End timing an operation and return duration"""
        if name not in self.start_times:
            logger.warning(f"Operation {name} was never started")
            return None
            
        duration = time.time() - self.start_times[name]
        self.operations[name] = duration
        logger.debug(f"Operation {name} took {duration:.3f}s")
        return duration
        
    def get_duration(self, name: str) -> Optional[float]:
        """Get duration of a completed operation"""
        return self.operations.get(name)
        
    def reset(self) -> None:
        """Reset all timings"""
        self.operations.clear()
        self.start_times.clear()

monitor = PerformanceMonitor()
