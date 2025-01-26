"""
Configuration settings for PS SimC Parser
"""
from typing import Dict, Any
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
TESTS_DIR = BASE_DIR / 'tests'
DOCS_DIR = BASE_DIR / 'docs'

# API settings
API_VERSION = '1.0.0'
API_COMPATIBILITY = ['1.0.x']

# Parser settings
PARSER_SETTINGS: Dict[str, Any] = {
    'strict_mode': True,
    'allow_unknown_spells': False,
    'allow_unknown_resources': False,
    'validate_mappings': True,
}

# Generator settings
GENERATOR_SETTINGS: Dict[str, Any] = {
    'optimize_code': True,
    'add_comments': True,
    'format_output': True,
}

# Debug settings
DEBUG = os.getenv('PS_DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('PS_LOG_LEVEL', 'INFO')

# Cache settings
CACHE_ENABLED = True
CACHE_SIZE = 1000
CACHE_TTL = 3600  # 1 hour

# Performance settings
PERFORMANCE_MONITORING = True
PROFILING_ENABLED = DEBUG

# Test settings
TEST_SETTINGS: Dict[str, Any] = {
    'validate_lua': True,
    'check_performance': True,
    'coverage_minimum': 80,
}

# Documentation settings
DOCS_SETTINGS: Dict[str, Any] = {
    'auto_generate': True,
    'include_examples': True,
    'include_api_docs': True,
} 