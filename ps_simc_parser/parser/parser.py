"""
Parser for SimC APL files
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .apl import APLParser, Action

@dataclass
class ParserContext:
    """Context for parsing SimC APL"""
    variables: Dict[str, Any] = None
    action_lists: Dict[str, List[Action]] = None
    current_list: str = 'default'
    in_precombat: bool = False
    list_stack: List[str] = None
    max_recursion_depth: int = 10
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = {}
        if self.action_lists is None:
            self.action_lists = {}
        if self.list_stack is None:
            self.list_stack = []

class ParseError(Exception):
    """Custom exception for parsing errors"""
    pass

class Parser:
    """Parser for SimC APL files"""
    
    def __init__(self, context: Optional[ParserContext] = None):
        self.context = context or ParserContext()
        self.apl_parser = APLParser()
        
    def parse(self, content: str) -> ParserContext:
        """Parse SimC APL content into action lists"""
        try:
            # Parse actions using APLParser
            actions = self.apl_parser.parse(content)
            
            # Add actions to default list
            if 'default' not in self.context.action_lists:
                self.context.action_lists['default'] = []
            self.context.action_lists['default'].extend(actions)
            
            return self.context
            
        except Exception as e:
            # Re-raise any parsing errors
            raise ParseError(f"Failed to parse APL: {str(e)}")
            
    def _validate_dependencies(self, actions: List[Action]):
        """Validate action dependencies"""
        self.apl_parser._validate_dependencies(actions)
        
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
