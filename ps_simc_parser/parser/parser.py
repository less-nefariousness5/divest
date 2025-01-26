"""
Parser for SimC APL files
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .actions import Action, ActionList

@dataclass
class ParserContext:
    """Context for parsing SimC APL"""
    class_name: str
    spec_name: str
    role: str
    level: int = 70
    talents: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.talents is None:
            self.talents = {}

class ParseError(Exception):
    """Custom exception for parsing errors"""
    pass

class Parser:
    """Parser for SimC APL files"""
    
    def __init__(self, context: Optional[ParserContext] = None):
        self.context = context or ParserContext(
            class_name='demonhunter',
            spec_name='vengeance',
            role='tank'
        )
        self.action_lists: Dict[str, ActionList] = {}
        
    def parse(self, content: str) -> Dict[str, ActionList]:
        """Parse SimC APL content into action lists"""
        try:
            lines = content.strip().split('\n')
            current_list = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if line.startswith('actions'):
                    action_list_name, action = self._parse_action_line(line)
                    
                    if action_list_name not in self.action_lists:
                        self.action_lists[action_list_name] = ActionList(action_list_name)
                        
                    if action:
                        self.action_lists[action_list_name].add_action(action)
                        
            return self.action_lists
            
        except Exception as e:
            raise ParseError(f"Failed to parse APL: {str(e)}")
            
    def _parse_action_line(self, line: str) -> tuple[str, Optional[Action]]:
        """Parse a single action line"""
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')]
            
        # Split into parts
        parts = line.split('=', 1)
        if len(parts) != 2:
            return 'default', None
            
        action_path, action_str = parts
        
        # Get action list name
        path_parts = action_path.split('.')
        if len(path_parts) > 2:
            list_name = path_parts[1]
        else:
            list_name = 'default'
            
        # Parse action
        if not action_str:
            return list_name, None
            
        try:
            action = Action(action_str)
            return list_name, action
        except Exception as e:
            raise ParseError(f"Failed to parse action '{action_str}': {str(e)}")
            
    def _parse_conditions(self, condition_str: str) -> List[str]:
        """Parse conditions from a condition string"""
        if not condition_str:
            return []
            
        conditions = []
        current = ''
        paren_count = 0
        
        for char in condition_str:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == '&' and paren_count == 0:
                if current:
                    conditions.append(current.strip())
                current = ''
                continue
                
            current += char
            
        if current:
            conditions.append(current.strip())
            
        return conditions
        
    def _parse_resource_expression(self, expr: str) -> Dict[str, Any]:
        """Parse a resource expression"""
        if not expr:
            return {}
            
        result = {}
        
        # Handle resource.deficit
        if '.deficit' in expr:
            resource = expr.split('.deficit')[0]
            result['type'] = 'deficit'
            result['resource'] = resource
        # Handle basic resource check
        else:
            resource = expr.split('<')[0].split('>')[0].split('=')[0]
            result['type'] = 'current'
            result['resource'] = resource
            
        # Get comparison and value
        if '>=' in expr:
            result['comparison'] = '>='
            result['value'] = float(expr.split('>=')[1])
        elif '<=' in expr:
            result['comparison'] = '<='
            result['value'] = float(expr.split('<=')[1])
        elif '>' in expr:
            result['comparison'] = '>'
            result['value'] = float(expr.split('>')[1])
        elif '<' in expr:
            result['comparison'] = '<'
            result['value'] = float(expr.split('<')[1])
        elif '=' in expr:
            result['comparison'] = '='
            result['value'] = float(expr.split('=')[1])
            
        return result
        
    def _parse_target_expression(self, expr: str) -> Dict[str, Any]:
        """Parse a target expression"""
        if not expr or not expr.startswith('target.'):
            return {}
            
        result = {}
        expr = expr[7:]  # Remove 'target.'
        
        # Handle time_to_die
        if expr.startswith('time_to_die'):
            result['type'] = 'time_to_die'
            expr = expr[11:]  # Remove 'time_to_die'
        # Handle health
        elif expr.startswith('health.pct'):
            result['type'] = 'health_percent'
            expr = expr[10:]  # Remove 'health.pct'
        # Handle distance
        elif expr.startswith('distance'):
            result['type'] = 'distance'
            expr = expr[8:]  # Remove 'distance'
            
        # Get comparison and value
        if '>=' in expr:
            result['comparison'] = '>='
            result['value'] = float(expr.split('>=')[1])
        elif '<=' in expr:
            result['comparison'] = '<='
            result['value'] = float(expr.split('<=')[1])
        elif '>' in expr:
            result['comparison'] = '>'
            result['value'] = float(expr.split('>')[1])
        elif '<' in expr:
            result['comparison'] = '<'
            result['value'] = float(expr.split('<')[1])
        elif '=' in expr:
            result['comparison'] = '='
            result['value'] = float(expr.split('=')[1])
            
        return result
