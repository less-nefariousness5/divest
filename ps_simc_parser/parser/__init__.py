"""
Core parser module for PS SimC Parser
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from .apl import APLParser
from .actions import ActionParser
import re

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
    max_recursion_depth: int = 10

class Parser:
    """Main parser class for converting SimC APL to PS Lua"""
    
    def __init__(self):
        self.apl_parser = APLParser()
        self.action_parser = ActionParser()
        self.context = ParserContext(
            variables={},
            action_lists={},
            current_list="default",
            in_precombat=False,
            list_stack=[]
        )

    def parse_file(self, input_file: str) -> ParserContext:
        """Parse a SimC file into a ParserContext with organized action lists"""
        with open(input_file, 'r') as f:
            simc_content = f.read()
        return self.parse(simc_content)

    def parse(self, input_str: str) -> ParserContext:
        """Parse a SimC string into a ParserContext with organized action lists"""
        # Reset context
        self.context = ParserContext(
            variables={},
            action_lists={},
            current_list="default",
            in_precombat=False,
            list_stack=[]
        )
        
        # Handle string input
        if isinstance(input_str, str):
            for line_num, line in enumerate(input_str.splitlines(), 1):
                try:
                    parsed = self.parse_line(line.strip())
                    if parsed:
                        current_list = self.context.current_list
                        if current_list not in self.context.action_lists:
                            self.context.action_lists[current_list] = []
                        self.context.action_lists[current_list].append(parsed)
                except ParseError as e:
                    raise ParseError(f"Error on line {line_num}: {str(e)}")
        # Handle list input
        elif isinstance(input_str, list):
            self.context.action_lists["default"] = input_str
        else:
            raise ParseError(f"Invalid input type: {type(input_str)}")
        
        return self.context

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
            'type': 'spell',  # Changed from 'action' to 'spell'
            'name': value.lstrip('/'),  # Remove leading / from spell name
            'conditions': [],
            'args': {}
        }
        
        # Parse parameters
        for param in params:
            if '=' in param:
                key, val = param.split('=', 1)
                action_dict['args'][key] = val.strip()
                
        return action_dict

    def _parse_action_list_call(self, params: List[str]) -> Dict:
        """Parse a call_action_list action"""
        result = {'type': 'call_action_list'}
        conditions = []
        
        for param in params:
            if param.startswith('name='):
                result['list_name'] = param.split('=', 1)[1]
            elif param.startswith('if='):
                conditions.extend(self._parse_conditions(param[3:]))
                
        if 'list_name' not in result:
            raise ParseError("call_action_list missing required name parameter")
            
        # Check recursion depth
        if result['list_name'] in self.context.list_stack:
            if len(self.context.list_stack) >= self.context.max_recursion_depth:
                raise ParseError(f"Maximum action list recursion depth exceeded: {result['list_name']}")
                
        result['conditions'] = conditions
        return result
        
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

    def get_variable_value(self, var_name: str) -> Optional[str]:
        """Get variable value respecting scope"""
        # Check current list scope first
        if (self.context.current_list in self.context.variables and 
            var_name in self.context.variables[self.context.current_list]):
            return self.context.variables[self.context.current_list][var_name]
            
        # Check parent scopes in reverse order
        for list_name in reversed(self.context.list_stack):
            if (list_name in self.context.variables and 
                var_name in self.context.variables[list_name]):
                return self.context.variables[list_name][var_name]
                
        # Check global scope
        if ('default' in self.context.variables and 
            var_name in self.context.variables['default']):
            return self.context.variables['default'][var_name]
            
        return None

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

    def generate_lua(self, actions: List[Dict], output_file: str) -> None:
        """Generate PS Lua code from parsed actions and write to file"""
        lua_code = self.action_parser.generate_lua(actions)
        with open(output_file, 'w') as f:
            f.write(lua_code)
