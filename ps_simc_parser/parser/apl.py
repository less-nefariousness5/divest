"""
APL (Action Priority List) parser for PS SimC Parser
"""
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
import re
import click
from .exceptions import (
    ParserError, SyntaxError, CircularReferenceError,
    DependencyError, ComplexityError, ValidationError
)
from .parser_context import ParserContext

@dataclass
class APLAction:
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
            
        # Parse action and conditions
        action_part = parts[0]
        condition_parts = parts[1:] if len(parts) > 1 else []
        
        # Parse action part
        if '=' in action_part:
            action_name, value = action_part.split('=', 1)
            action_name = action_name.rstrip('+')  # Remove + from actions+=
            
            # Handle action lists
            if action_name.startswith('actions'):
                list_name = action_name[7:] or "default"  # actions.name or just actions
                if list_name.startswith('.'):
                    list_name = list_name[1:]
                self.action_list_name = list_name
                
            # Handle variables
            if value == 'variable':
                self.spell_name = 'variable'
                for part in condition_parts:
                    if part.startswith('name='):
                        self.var_name = part[5:]
                    elif part.startswith('value='):
                        self.var_value = part[6:]
                    elif part.startswith('op='):
                        self.var_op = part[3:]
            else:
                self.spell_name = value.lstrip('/')
                
        # Parse conditions
        for part in condition_parts:
            if part.startswith('if='):
                self.conditions = self._parse_conditions(part[3:])
                
    def _parse_conditions(self, condition_str: str) -> List[str]:
        """Parse conditions from a condition string"""
        if not condition_str:
            return []
            
        # Split on & and |, preserving them as operators
        conditions = []
        current = []
        for char in condition_str:
            if char in '&|':
                if current:
                    conditions.append(''.join(current).strip())
                    current = []
                conditions.append(char)
            else:
                current.append(char)
                
        if current:
            conditions.append(''.join(current).strip())
            
        return conditions
        
    def has_conditions(self) -> bool:
        """Check if this action has conditions"""
        return bool(self.conditions)
        
    def __str__(self) -> str:
        """String representation of the action"""
        parts = []
        if self.action_list_name:
            parts.append(f"actions.{self.action_list_name}")
        else:
            parts.append("actions")
            
        if self.spell_name == 'variable':
            parts.append(f"variable,name={self.var_name}")
            if self.var_value:
                parts.append(f"value={self.var_value}")
            if self.var_op:
                parts.append(f"op={self.var_op}")
        else:
            parts.append(self.spell_name)
            
        if self.conditions:
            parts.append(f"if={'&'.join(self.conditions)}")
            
        return ','.join(parts)

class APLParser:
    """Parser for SimC APL syntax"""
    
    def __init__(self):
        """Initialize parser"""
        self.variables: Dict[str, Any] = {}
        self.dependencies: Set[str] = set()
        self.max_complexity = 50  # Maximum number of conditions in a single APL
        self.known_spells: Set[str] = set()  # Will be populated from context
        self.variable_references: Dict[str, Set[str]] = {}  # Track variable references
        self.debug = True  # Enable debug output
        
    def parse(self, content: str, context: ParserContext) -> List[APLAction]:
        """Parse SimC APL content into intermediate representation"""
        # Reset state
        self.variables.clear()
        self.dependencies.clear()
        self.variable_references.clear()
        
        # Get known spells from context
        self.known_spells = context.spec.get('spells', set())
        
        # Split content into lines and remove comments
        lines = content.strip().split('\n')
        actions = []
        line_number = 0
        
        for line in lines:
            line_number += 1
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Skip character configuration lines
            if '=' in line and not any(line.startswith(prefix) for prefix in ['actions', 'variable']):
                continue
                
            # Parse action line
            try:
                action = APLAction(line, line_number=line_number)
                
                # Validate spell name
                if action.spell_name and action.spell_name != 'variable' and action.spell_name not in self.known_spells:
                    if self.debug:
                        click.echo(f"Warning: Unknown spell '{action.spell_name}' at line {line_number}", err=True)
                    
                # Check for variable references
                if action.var_name:
                    self._check_circular_references(action.var_name, action.var_value or '')
                    
                # Track dependencies
                if action.conditions:
                    self.dependencies.update(action.conditions)
                    
                    # Check complexity
                    if len(action.conditions) > self.max_complexity:
                        raise ComplexityError(
                            f"Too many conditions ({len(action.conditions)}) in action at line {line_number}"
                        )
                        
                actions.append(action)
                
            except ParserError as e:
                # Add line number to error
                e.line_number = line_number
                raise
                
        # Validate all dependencies are satisfied
        for dep in self.dependencies:
            if dep not in self.variables and not any(
                dep.startswith(prefix) for prefix in ('spell', 'buff', 'debuff', 'talent', 'variable')
            ):
                if self.debug:
                    click.echo(f"Warning: Unsatisfied dependency '{dep}'", err=True)
                
        return actions
        
    def _check_circular_references(self, var_name: str, value: str):
        """Check for circular variable references"""
        # Track dependencies for this variable
        self.variable_references[var_name] = set()
        
        # Find all variable references in the value
        var_refs = re.findall(r'variable\.([\w_]+)', value)
        for ref in var_refs:
            self.variable_references[var_name].add(ref)
            
            # Check for circular reference
            if ref == var_name:
                raise CircularReferenceError(f"Variable {var_name} references itself")
                
            # Check for indirect circular reference
            if ref in self.variable_references:
                for indirect_ref in self.variable_references[ref]:
                    if indirect_ref == var_name:
                        raise CircularReferenceError(
                            f"Circular reference detected: {var_name} -> {ref} -> {var_name}"
                        )
