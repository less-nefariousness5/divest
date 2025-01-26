"""
APL (Action Priority List) parser for PS SimC Parser
"""
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
import re
from .exceptions import (
    ParserError, SyntaxError, CircularReferenceError,
    DependencyError, ComplexityError, ValidationError
)

@dataclass
class Action:
    """Represents a single action in the SimC APL"""
    action_str: str
    line_number: int = 0
    conditions: List[str] = field(default_factory=list)
    spell_name: Optional[str] = None
    target: Optional[str] = None
    var_name: Optional[str] = None
    var_value: Optional[str] = None
    var_op: Optional[str] = None
    pool_for_next: bool = False
    pool_extra_amount: Optional[int] = None
    action_list_name: Optional[str] = None
    
    def __post_init__(self):
        self._parse_action()
        
    def _parse_action(self):
        """Parse the action string into components"""
        # Split into parts and handle whitespace
        parts = []
        current_part = []
        in_quotes = False
        paren_level = 0
        
        for char in self.action_str:
            if char == '"':
                in_quotes = not in_quotes
                current_part.append(char)
            elif char == ',' and not in_quotes and paren_level == 0:
                parts.append(''.join(current_part).strip())
                current_part = []
            else:
                if char == '(':
                    paren_level += 1
                elif char == ')':
                    paren_level -= 1
                current_part.append(char)
                
        if current_part:
            parts.append(''.join(current_part).strip())
        
        # First part is the action name/type
        action_type = parts[0].strip('/')
        self.spell_name = action_type
        
        # Validate action name
        if not action_type:
            raise SyntaxError("Missing action name")
            
        if not re.match(r'^[a-zA-Z0-9_]+$', action_type):
            raise ValidationError(f"Invalid characters in action name: {action_type}")
        
        # Parse remaining parameters
        for part in parts[1:]:
            if '=' not in part:
                continue
                
            key, value = [p.strip() for p in part.split('=', 1)]
            
            if key == 'if':
                # Check for double equals
                if value.startswith('='):
                    raise SyntaxError(f"Invalid operator: double equals (==)")
                # Check for missing value after operator
                if any(value.endswith(op) for op in ['>', '<', '=', '!', '&', '|']):
                    raise SyntaxError(f"Missing value after operator")
                    
                self.conditions = self._parse_conditions(value)
            elif key == 'name':
                self.var_name = value
            elif key == 'value':
                self.var_value = value
            elif key == 'op':
                self.var_op = value
            elif key == 'for_next':
                self.pool_for_next = value.lower() == 'true'
            elif key == 'extra_amount':
                try:
                    self.pool_extra_amount = int(value)
                except ValueError:
                    raise SyntaxError(f"Invalid extra_amount value: {value}")
    
    def _parse_conditions(self, condition_str: str) -> List[str]:
        """Parse conditions from a condition string"""
        # Normalize whitespace
        condition_str = re.sub(r'\s+', ' ', condition_str.strip())
        
        # Check for invalid operators
        if any(op in condition_str for op in ['!!', '><', '~~']):
            raise SyntaxError(f"Invalid operator in condition: {condition_str}")
        
        # Check for unmatched parentheses
        if condition_str.count('(') != condition_str.count(')'):
            raise SyntaxError(f"Unmatched parentheses in condition: {condition_str}")
        
        # Check condition complexity
        if condition_str.count('(') > 10 or condition_str.count('&') > 10:
            raise ComplexityError(f"Condition too complex (too many operators or nested too deeply): {condition_str}")
        
        # Split conditions
        conditions = []
        current = []
        paren_level = 0
        
        for char in condition_str:
            if char == '(':
                paren_level += 1
                current.append(char)
            elif char == ')':
                paren_level -= 1
                current.append(char)
            elif char == '&' and paren_level == 0:
                conditions.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
        
        if current:
            conditions.append(''.join(current).strip())
        
        # Normalize conditions
        conditions = [re.sub(r'\s+', ' ', cond.strip()) for cond in conditions]
        conditions = [re.sub(r'\s*([<>=&|])\s*', r'\1', cond) for cond in conditions]
        
        return conditions
        
    def has_conditions(self) -> bool:
        """Check if this action has conditions"""
        return bool(self.conditions)

    def __str__(self):
        """String representation of the action"""
        parts = [self.spell_name]
        if self.conditions:
            parts.append(f"if={' & '.join(self.conditions)}")
        if self.var_name:
            parts.append(f"name={self.var_name}")
        if self.var_value:
            parts.append(f"value={self.var_value}")
        return ','.join(parts)

class APLParser:
    """Parser for SimC APL syntax"""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.dependencies: Set[str] = set()
        self.max_complexity = 50  # Maximum number of conditions in a single APL
        self.known_spells: Set[str] = {'auto_attack', 'spell_name', 'valid_spell', 'another_spell'}  # Set of known spell names
        self.variable_references: Dict[str, Set[str]] = {}  # Track variable references
        
    def _check_circular_references(self, var_name: str, value: str):
        """Check for circular variable references"""
        if var_name not in self.variable_references:
            self.variable_references[var_name] = set()
            
        # Extract referenced variables
        refs = re.findall(r'variable\.([a-zA-Z0-9_]+)', value)
        self.variable_references[var_name].update(refs)
        
        # Check for circular references
        seen = {var_name}
        to_check = list(refs)
        
        while to_check:
            current = to_check.pop(0)
            if current in seen:
                raise CircularReferenceError(f"Circular reference detected: {' -> '.join(seen)} -> {current}")
            seen.add(current)
            if current in self.variable_references:
                to_check.extend(self.variable_references[current])

    def parse(self, content: str, context: Any = None) -> List[Action]:
        """Parse SimC APL content into intermediate representation"""
        if not content.strip():
            raise ValidationError("Empty input")
            
        actions = []
        continued_line = ""
        line_number = 0
        
        for line in content.splitlines():
            line_number += 1
            # Handle line continuation
            if continued_line:
                line = continued_line + line.strip()
                continued_line = ""
            else:
                line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith(('#', '//')):
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
                
            try:
                # Parse the action line
                if not line.startswith(('actions', 'variable')):
                    raise SyntaxError(f"Line must start with 'actions' or 'variable'")
                    
                # Split into base and arguments
                if '=' not in line:
                    raise SyntaxError(f"Missing '=' in line")
                    
                base, args_str = line.split('=', 1)
                base = base.strip()
                args_str = args_str.strip()
                
                # Handle action list append syntax
                if base == 'actions+/' or base == 'actions+':
                    base = 'actions'
                    args_str = args_str.lstrip('/')
                
                # Validate action format
                if not args_str:
                    raise SyntaxError("Empty action")
                
                try:
                    # Create action object
                    action = Action(args_str, line_number=line_number)
                    
                    # Check for variable references
                    if action.var_name:
                        self._check_circular_references(action.var_name, action.var_value or '')
                    
                    # Check complexity
                    if len(actions) > self.max_complexity:
                        raise ComplexityError("APL contains too many actions")
                    
                    # Validate spell dependencies
                    if action.spell_name and self.known_spells and action.spell_name not in self.known_spells:
                        raise DependencyError(f"Unknown spell: {action.spell_name}")
                    
                    for condition in action.conditions:
                        if 'spell.' in condition or 'buff.' in condition:
                            spell_name = condition.split('.')[1].split('.')[0]
                            if spell_name not in self.known_spells:
                                raise DependencyError(f"Unknown spell or buff: {spell_name}")
                    
                    actions.append(action)
                    
                except (SyntaxError, ValidationError, CircularReferenceError, ComplexityError, DependencyError) as e:
                    # Add line information to error
                    raise type(e)(f"Line {line_number}: {str(e)}\n  {line}")
                
            except (SyntaxError, ValidationError, CircularReferenceError, ComplexityError, DependencyError) as e:
                # Add line information to error
                raise type(e)(f"Line {line_number}: {str(e)}\n  {line}")
            except Exception as e:
                # Wrap unknown errors
                raise ParserError(f"Line {line_number}: {str(e)}\n  {line}")
        
        return actions
