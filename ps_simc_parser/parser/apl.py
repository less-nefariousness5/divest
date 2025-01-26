"""
APL (Action Priority List) parser for PS SimC Parser
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Action:
    """Represents a single APL action"""
    name: str
    conditions: List[str]
    args: Dict[str, Any]

class APLParser:
    """Parser for SimC APL syntax"""
    
    def __init__(self):
        self.current_action_list = []
        self.variables = {}

    def parse(self, content: str, context: Any) -> List[Action]:
        """Parse SimC APL content into intermediate representation"""
        actions = []
        continued_line = ""
        
        for line in content.splitlines():
            # Handle line continuation
            if continued_line:
                line = continued_line + line.strip()
                continued_line = ""
            else:
                line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Handle comments
            if line.startswith(('#', '//')):
                continue
                
            # Remove inline comments
            if '#' in line:
                line = line.split('#')[0].strip()
            if '//' in line:
                line = line.split('//')[0].strip()
                
            # Handle line continuation
            if line.endswith('\\'):
                continued_line = line[:-1]
                continue
                
            # Parse the action line
            if not line.startswith(('actions', 'variable')):
                raise ValueError(f"Invalid syntax: Line must start with 'actions' or 'variable', got: {line}")
                
            # Split into base and arguments
            if '=' not in line:
                raise ValueError(f"Invalid syntax: Missing '=' in line: {line}")
                
            base, args_str = line.split('=', 1)
            base = base.strip()
            
            # Handle action list append syntax
            if base == 'actions+/' or base == 'actions+':
                base = 'actions'
                args_str = args_str.lstrip('/')
                
            # Parse arguments
            args = {}
            conditions = []
            
            if args_str:
                parts = [p.strip() for p in args_str.split(',')]
                action_name = parts[0]
                
                # Handle variable operations
                if action_name == 'variable':
                    var_args = {}
                    for part in parts[1:]:
                        if not part:
                            continue
                        
                        if '=' not in part:
                            continue
                            
                        key, value = part.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == 'if':
                            conditions.extend([c.strip() for c in value.split('&') if c.strip()])
                        else:
                            var_args[key] = value
                    
                    # Ensure required variable fields are present
                    if 'name' not in var_args:
                        raise ValueError(f"Variable must have name: {line}")
                    
                    # For reset operation, default is required
                    if var_args.get('op') == 'reset' and 'default' not in var_args:
                        raise ValueError(f"Reset operation requires default value: {line}")
                    
                    # For other operations, value is required
                    if var_args.get('op') != 'reset' and 'value' not in var_args:
                        raise ValueError(f"Operation requires value: {line}")
                    
                    args = var_args
                else:
                    # Handle regular action arguments
                    for part in parts[1:]:
                        if not part:
                            raise ValueError(f"Invalid syntax: Empty argument in line: {line}")
                            
                        if part.startswith('if='):
                            # Handle conditions
                            cond_str = part[3:]
                            if not cond_str:
                                raise ValueError(f"Invalid syntax: Empty condition in line: {line}")
                                
                            # Validate condition operators
                            if any(op in cond_str for op in ['&&', '||']):
                                raise ValueError(f"Invalid syntax: Use '&' for AND, '|' for OR in conditions: {line}")
                                
                            if cond_str.startswith(('&', '|')) or cond_str.endswith(('&', '|')):
                                raise ValueError(f"Invalid syntax: Invalid operator position in conditions: {line}")
                                
                            conditions.extend([c.strip() for c in cond_str.split('&') if c.strip()])
                        else:
                            # Handle regular arguments
                            if '=' not in part:
                                raise ValueError(f"Invalid syntax: Missing '=' in argument: {part}")
                                
                            arg_parts = part.split('=')
                            if len(arg_parts) != 2:
                                raise ValueError(f"Invalid syntax: Invalid argument format: {part}")
                                
                            args[arg_parts[0].strip()] = arg_parts[1].strip()
            
            action = Action(name=action_name, conditions=conditions, args=args)
            actions.append(action)
            
        return actions
