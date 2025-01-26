"""
API mapping module for PS SimC Parser
Handles conversion between SimC concepts and PS API
"""

from .mapping import (
    convert_spell,
    convert_condition,
    convert_resource,
    convert_buff,
    convert_target,
)

__all__ = [
    'convert_spell',
    'convert_condition',
    'convert_resource',
    'convert_buff',
    'convert_target',
]
