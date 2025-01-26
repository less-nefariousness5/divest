"""
Context module for PS SimC Parser
"""
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ParserContext:
    """Context object for parsing state"""
    variables: Dict[str, Dict[str, str]] = None  # Scoped variables: {scope: {name: value}}
    action_lists: Dict[str, List[Dict]] = None   # Action lists with full parsed actions
    current_list: str = "default"
    in_precombat: bool = False
    list_stack: List[str] = None  # Track nested action list calls
    spec: Dict[str, Any] = None
    max_recursion_depth: int = 10
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = {}
        if self.action_lists is None:
            self.action_lists = {}
        if self.list_stack is None:
            self.list_stack = []
