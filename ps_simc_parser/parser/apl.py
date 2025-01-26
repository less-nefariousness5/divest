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
                
        # Add final part
        if current_part:
            parts.append(''.join(current_part).strip())
            
        # Parse first part as action name
        if not parts:
            raise SyntaxError("Empty action string")
            
        action_part = parts[0]
        if '=' in action_part:
            # Handle variable assignment
            var_parts = action_part.split('=', 1)
            if len(var_parts) != 2:
                raise SyntaxError(f"Invalid variable assignment: {action_part}")
                
            self.var_name = var_parts[0].strip()
            self.var_value = var_parts[1].strip()
            
        elif action_part.startswith('/'):
            # Handle spell cast
            self.spell_name = action_part[1:].strip()  # Remove leading /
            
        else:
            # Handle other actions
            self.spell_name = action_part.strip()
            
        # Parse remaining parts
        for part in parts[1:]:
            if not part:
                continue
                
            # Handle conditions
            if part.startswith('if='):
                self._parse_conditions(part[3:])  # Skip 'if='
                
            # Handle target specification
            elif part.startswith('target='):
                self.target = part[7:]  # Skip 'target='
                
            # Handle variable operation
            elif part.startswith('op='):
                self.var_op = part[3:]  # Skip 'op='
                
            # Handle pool resource
            elif part == 'for_next=1':
                self.pool_for_next = True
            elif part.startswith('extra_amount='):
                try:
                    self.pool_extra_amount = int(part[13:])  # Skip 'extra_amount='
                except ValueError:
                    raise SyntaxError(f"Invalid pool extra amount: {part}")
                    
            # Handle action list
            elif part.startswith('name='):
                self.action_list_name = part[5:]  # Skip 'name='
                
    def _parse_conditions(self, condition_str: str):
        """Parse conditions from a condition string"""
        # Split on boolean operators while preserving them
        parts = re.split(r'([&|])', condition_str)
        
        # Process each part
        for part in parts:
            part = part.strip()
            if part and part not in ('&', '|'):
                self.conditions.append(part)
                
    def has_conditions(self) -> bool:
        """Check if this action has conditions"""
        return bool(self.conditions)
        
    def __str__(self) -> str:
        """String representation of the action"""
        parts = []
        
        # Add action/spell name
        if self.var_name:
            parts.append(f"variable,name={self.var_name}")
            if self.var_value:
                parts.append(f"value={self.var_value}")
            if self.var_op:
                parts.append(f"op={self.var_op}")
        elif self.spell_name:
            parts.append(self.spell_name)
            
        # Add conditions
        if self.conditions:
            parts.append(f"if={'&'.join(self.conditions)}")
            
        # Add target
        if self.target:
            parts.append(f"target={self.target}")
            
        # Add pool options
        if self.pool_for_next:
            parts.append("for_next=1")
        if self.pool_extra_amount is not None:
            parts.append(f"extra_amount={self.pool_extra_amount}")
            
        # Add action list name
        if self.action_list_name:
            parts.append(f"name={self.action_list_name}")
            
        return ','.join(parts)

@dataclass
class ParserContext:
    """Context for parsing SimC APL"""
    spec: Dict[str, Any]
    
    def __post_init__(self):
        """Initialize parser context"""
        self.valid_actions = set()
        
        # Add spells from spec
        if 'spells' in self.spec:
            self.valid_actions.update(self.spec['spells'])
            
        # Add special actions
        self.valid_actions.update([
            'auto_attack',
            'variable',
            'pool_resource',
            'call_action_list',
            'run_action_list',
        ])

class APLParser:
    """Parser for SimC APL syntax"""
    
    def __init__(self):
        """Initialize parser"""
        self.variables: Dict[str, Any] = {}
        self.dependencies: Set[str] = set()
        self.max_complexity = 50  # Maximum number of conditions in a single APL
        self.known_spells: Set[str] = set()  # Will be populated from context
        self.variable_references: Dict[str, Set[str]] = {}  # Track variable references
        
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
                        
    def parse(self, content: str, context: ParserContext) -> List[APLAction]:
        """Parse SimC APL content into intermediate representation"""
        # Reset state
        self.variables.clear()
        self.dependencies.clear()
        self.variable_references.clear()
        
        # Get known spells from context
        self.known_spells = context.valid_actions
        
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
                
            # Parse action line
            try:
                action = APLAction(line, line_number=line_number)
                
                # Validate spell name
                if action.spell_name and action.spell_name not in self.known_spells:
                    raise ValidationError(f"Unknown spell: {action.spell_name}")
                    
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
                dep.startswith(prefix) for prefix in ('spell', 'buff', 'debuff', 'talent')
            ):
                raise DependencyError(f"Unsatisfied dependency: {dep}")
                
        return actions
