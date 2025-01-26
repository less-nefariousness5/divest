"""
Compatibility checker for PS SimC Parser
"""
import logging
from typing import Optional
from ..config import API_VERSION

logger = logging.getLogger(__name__)

class CompatibilityChecker:
    """Check compatibility between parser and PS API versions"""
    
    @staticmethod
    def check_version(version: Optional[str] = None) -> bool:
        """Check if the given API version is compatible"""
        if not version:
            version = API_VERSION
            
        # For now, we just log the version check
        logger.info(f"Checking compatibility for API version {version}")
        return True  # All versions are compatible for now

    @staticmethod
    def get_supported_versions() -> list:
        """Get list of supported API versions"""
        return [API_VERSION]  # Only current version for now

compatibility = CompatibilityChecker()
