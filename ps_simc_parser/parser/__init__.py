"""
Core parser module for PS SimC Parser
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re
import click
from .apl import APLParser, APLAction, ParserContext
from .actions import ActionParser, Action
from ..utils.constants import SUPPORTED_SPECS

class ParseError(Exception):
    """Exception raised for parsing errors"""
    pass

@dataclass
class ParserContext:
    """Context object for parsing state"""
    variables: Dict[str, Dict[str, str]]  # Scoped variables: {scope: {name: value}}
    action_lists: Dict[str, List[Dict]]   # Action lists with full parsed actions
    current_list: str
    in_precombat: bool
    list_stack: List[str]  # Track nested action list calls
    spec: Dict[str, Any]
    max_recursion_depth: int = 10

class Parser:
    """Parser class for PS SimC Parser."""
    
    def __init__(self):
        """Initialize parser."""
        self.specs = SUPPORTED_SPECS
        self._spec = None
        self.apl_parser = APLParser()
        self.action_parser = ActionParser()
        
    def parse(self, content: str) -> ParserContext:
        """Parse SimC APL content and return a ParserContext.
        This is the main entry point for parsing."""
        if self.spec is None:
            raise ValueError("Specialization must be set before parsing")
            
        self.context = ParserContext(
            variables={},
            action_lists={},
            current_list="default",
            in_precombat=False,
            list_stack=[],
            spec=self.specs[self.spec]
        )
        
        # Parse the content
        for line_num, line in enumerate(content.splitlines(), 1):
            try:
                parsed = self.parse_line(line.strip())
                if parsed:
                    current_list = self.context.current_list
                    if current_list not in self.context.action_lists:
                        self.context.action_lists[current_list] = []
                    self.context.action_lists[current_list].append(parsed)
            except ParseError as e:
                raise ParseError(f"Error on line {line_num}: {str(e)}")
                
        return self.context

    def parse_file_content(self, content: str) -> ParserContext:
        """Parse SimC APL content."""
        return self.parse(content)
        
    @property
    def spec(self):
        return self._spec
        
    @spec.setter
    def spec(self, value):
        if value is not None and value not in self.specs:
            raise ValueError(f"Unsupported specialization: {value}")
        self._spec = value
        
    def parse_file(self, input_file: str) -> List[Action]:
        """Parse a SimC APL file."""
        if self.spec is None:
            raise ValueError("Specialization must be set before parsing")
            
        with open(input_file, 'r') as f:
            content = f.read()
            
        return self.parse_file_content(content)
        
    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single line of SimC input into a dictionary
        
        Returns:
            Dict with parsed action data or None for empty lines/comments
            
        Raises:
            ParseError: If the line has invalid syntax
        """
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            return None
            
        # Skip character configuration lines that don't contain actions
        if '=' in line and not any(line.startswith(prefix) for prefix in ['actions', 'variable']):
            return None
            
        # Split into action and parameters
        parts = line.split(',')
        action_part = parts[0]
        params = parts[1:] if len(parts) > 1 else []
        
        # Handle standalone variable definitions
        if action_part == 'variable':
            return self._parse_variable(params)
            
        # Handle action lists (actions=spell or actions+=spell)
        if '=' not in action_part:
            raise ParseError(f"Invalid syntax: {line}")
            
        action_name, value = action_part.split('=', 1)
        action_name = action_name.rstrip('+')  # Remove + from actions+=
        
        # Update current action list
        if action_name.startswith('actions'):
            list_name = action_name[7:] or "default"  # actions.name or just actions
            # Remove leading dot if present
            if list_name.startswith('.'):
                list_name = list_name[1:]
            self.context.current_list = list_name
            
            # Skip action list declarations without a spell
            if not value:
                return None
            
            # Handle variables in action lists
            if value == 'variable':
                return self._parse_variable(params)
        
        # Handle variables
        if value == 'variable':
            return self._parse_variable(params)
            
        # Handle regular actions
        action_dict = {
            'type': 'spell',  
            'name': value.lstrip('/'),  # Remove leading / from spell name
            'action': value.lstrip('/'),  # Add action field for Lua generator
            'conditions': [],
            'args': {}
        }
        
        # Parse parameters
        for param in params:
            if '=' in param:
                key, val = param.split('=', 1)
                action_dict['args'][key] = val.strip()
                
        return action_dict

    def _parse_variable(self, params: List[str]) -> Dict:
        """Parse variable definition parameters"""
        result = {'type': 'variable'}
        param_dict = {}
        
        for param in params:
            if '=' not in param:
                raise ParseError(f"Invalid variable parameter: {param}")
            key, value = param.split('=', 1)
            param_dict[key] = value
            
        if 'name' not in param_dict:
            raise ParseError("Variable must have name")
            
        result.update(param_dict)
        
        # Handle conditions
        if 'condition' in param_dict:
            result['conditions'] = [self._parse_conditions(param_dict['condition'])]
            del result['condition']
            
        # Handle values based on operation type
        if 'op' in param_dict:
            op = param_dict['op']
            if op == 'reset':
                if 'default' not in param_dict:
                    raise ParseError("Reset operation requires default value")
                result['value'] = param_dict['default']
            elif op == 'setif':
                if 'value' not in param_dict:
                    raise ParseError("Setif operation requires value")
                if 'value_else' in param_dict:
                    result['value_else'] = param_dict['value_else']
            elif op in ['set', 'add', 'sub', 'mul', 'div', 'max', 'min']:
                if 'value' not in param_dict:
                    raise ParseError(f"{op} operation requires value")
            else:
                raise ParseError(f"Unknown operation: {op}")
        elif 'value' not in param_dict:
            raise ParseError("Variable definition must have value or operation")
            
        return result

    def _parse_conditions(self, condition_str: str) -> List[Dict]:
        """Parse condition string into structured condition objects
        
        Handles:
        - Resource expressions (fury.deficit>40)
        - Buff states (.up, .down, .stack, .react)
        - Ternary operators (condition?value1:value2)
        - Compound conditions with & and |
        """
        if not condition_str:
            raise ParseError("Empty condition")
            
        conditions = []
        # Split on & first, then | for proper precedence
        for and_group in condition_str.split('&'):
            or_conditions = []
            for or_cond in and_group.split('|'):
                cond = or_cond.strip()
                if not cond:
                    raise ParseError("Empty condition in expression")
                    
                # Handle ternary operator
                if '?' in cond:
                    cond_obj = self._parse_ternary(cond)
                # Handle buff states
                elif any(suffix in cond for suffix in ['.up', '.down', '.stack', '.react']):
                    cond_obj = self._parse_buff_state(cond)
                # Handle resource checks
                elif any(resource in cond.lower() for resource in ['fury', 'energy', 'mana', 'rage']):
                    cond_obj = self._parse_resource(cond)
                # Handle basic comparisons
                else:
                    cond_obj = self._parse_basic_condition(cond)
                    
                or_conditions.append(cond_obj)
                
            if len(or_conditions) > 1:
                conditions.append({
                    'type': 'or',
                    'conditions': or_conditions
                })
            else:
                conditions.append(or_conditions[0])
                
        return conditions

    def _parse_ternary(self, cond: str) -> Dict:
        """Parse a ternary condition expression"""
        try:
            condition, values = cond.split('?', 1)
            true_val, false_val = values.split(':', 1)
            return {
                'type': 'ternary',
                'condition': self._parse_basic_condition(condition.strip()),
                'true_value': true_val.strip(),
                'false_value': false_val.strip()
            }
        except ValueError:
            raise ParseError(f"Invalid ternary expression: {cond}")

    def _parse_buff_state(self, cond: str) -> Dict:
        """Parse a buff state condition"""
        try:
            buff_name, state = cond.split('.', 1)
            result = {
                'type': 'buff',
                'name': buff_name,
                'state': state
            }
            
            # Handle stack/react count checks
            if '>' in state or '<' in state:
                for op in ['>=', '<=', '>', '<', '=']:
                    if op in state:
                        state_type, value = state.split(op, 1)
                        result.update({
                            'state_type': state_type,
                            'operator': op,
                            'value': int(value)
                        })
                        break
                        
            return result
        except ValueError:
            raise ParseError(f"Invalid buff state condition: {cond}")

    def _parse_resource(self, cond: str) -> Dict:
        """Parse a resource check condition"""
        try:
            # Handle resource.deficit>40 style
            if '.deficit' in cond:
                resource, rest = cond.split('.deficit', 1)
                is_deficit = True
            else:
                resource = cond.split('>')[0].split('<')[0].split('=')[0]
                rest = cond[len(resource):]
                is_deficit = False
                
            for op in ['>=', '<=', '>', '<', '=']:
                if op in rest:
                    value = rest.split(op, 1)[1]
                    return {
                        'type': 'resource',
                        'resource': resource.lower(),
                        'is_deficit': is_deficit,
                        'operator': op,
                        'value': float(value)
                    }
                    
            raise ParseError(f"Invalid resource check operator in: {cond}")
        except ValueError:
            raise ParseError(f"Invalid resource check condition: {cond}")

    def _parse_basic_condition(self, cond: str) -> Dict:
        """Parse a basic condition expression"""
        # Handle enemy count conditions
        if 'active_enemies' in cond:
            match = re.match(r'active_enemies([<>=]+)(\d+)', cond)
            if match:
                return {
                    'type': 'enemy_count',
                    'operator': match.group(1),
                    'value': int(match.group(2))
                }
                
        # Handle numeric comparisons
        match = re.match(r'(\w+)([<>=]+)(\d+)', cond)
        if match:
            return {
                'type': 'comparison',
                'target': match.group(1),
                'operator': match.group(2),
                'value': int(match.group(3))
            }
            
        # Handle boolean conditions
        return {
            'type': 'boolean',
            'value': cond
        }

    def generate_lua(self, actions: List[Action]) -> str:
        """Generate Lua code from parsed actions."""
        return self.action_parser.generate_lua(actions)

__all__ = [
    'Parser',
    'APLParser',
    'APLAction',
    'ParserContext',
    'ActionParser',
    'Action',
]
