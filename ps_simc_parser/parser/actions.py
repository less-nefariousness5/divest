"""
Action parser for converting SimC actions to PS Lua
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
import re

class ActionType(Enum):
    """Types of actions supported by the parser"""
    SPELL = auto()
    VARIABLE = auto()
    POOL = auto()
    CALL_ACTION_LIST = auto()
    RUN_ACTION_LIST = auto()

@dataclass
class Action:
    """Represents a single action in the SimC APL"""
    name: str
    conditions: List[str] = field(default_factory=list)
    args: Dict[str, Any] = field(default_factory=dict)
    comment: Optional[str] = None
    line_number: Optional[int] = None
    target_condition: Optional[str] = None
    cycle_targets: bool = False
    
    def __init__(self, action_str: str):
        """Parse action string into components"""
        self.name = ''
        self.conditions = []
        self.args = {}
        self.comment = None
        self.line_number = None
        self.target_condition = None
        self.cycle_targets = False
        
        # Split action string into parts
        parts = action_str.split(',')
        
        # Parse first part as name
        first_part = parts[0].strip()
        if first_part.startswith('/'):
            first_part = first_part[1:]  # Remove leading /
        self.name = first_part
        
        # Parse remaining parts
        for part in parts[1:]:
            if not part:
                continue
                
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if key == 'if':
                    # Split conditions on & and |
                    conditions = value.split('&')
                    self.conditions = [c.strip() for c in conditions if c.strip()]
                elif key == 'target_if':
                    self.target_condition = value
                elif key == 'cycle_targets':
                    self.cycle_targets = bool(int(value))
                else:
                    # Try to convert numeric values
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    self.args[key] = value
    
    @property
    def action_type(self) -> ActionType:
        """Get the type of this action"""
        if self.name.startswith('variable'):
            return ActionType.VARIABLE
        elif self.name.startswith('pool_resource'):
            return ActionType.POOL
        elif self.name.startswith('call_action_list'):
            return ActionType.CALL_ACTION_LIST
        elif self.name.startswith('run_action_list'):
            return ActionType.RUN_ACTION_LIST
        else:
            return ActionType.SPELL
            
    @property
    def spell_name(self) -> Optional[str]:
        """Get the spell name for this action"""
        if self.action_type == ActionType.SPELL:
            return self.name
        return None
        
    @property
    def var_name(self) -> Optional[str]:
        """Get the variable name for this action"""
        if self.action_type == ActionType.VARIABLE:
            return self.args.get('name')
        return None
        
    @property
    def var_value(self) -> Optional[str]:
        """Get the variable value for this action"""
        if self.action_type == ActionType.VARIABLE:
            return self.args.get('value')
        return None
        
    @property
    def var_op(self) -> Optional[str]:
        """Get the variable operation for this action"""
        if self.action_type == ActionType.VARIABLE:
            return self.args.get('op')
        return None
        
    @property
    def pool_for_next(self) -> bool:
        """Check if this action pools for next action"""
        if self.action_type == ActionType.POOL:
            return self.args.get('for_next', False)
        return False
        
    @property
    def pool_extra_amount(self) -> Optional[int]:
        """Get the extra amount to pool"""
        if self.action_type == ActionType.POOL:
            return self.args.get('extra_amount')
        return None
        
    @property
    def action_list_name(self) -> Optional[str]:
        """Get the name of the action list to call/run"""
        if self.action_type in (ActionType.CALL_ACTION_LIST, ActionType.RUN_ACTION_LIST):
            return self.args.get('name')
        return None
            
    @property
    def strict(self) -> bool:
        """Get strict flag for run_action_list"""
        if self.action_type == ActionType.RUN_ACTION_LIST:
            return bool(self.args.get('strict', False))
        return False
        
    def has_conditions(self) -> bool:
        """Check if this action has conditions"""
        return bool(self.conditions)
        
    def is_valid(self) -> bool:
        """Check if this action is valid"""
        # Basic validation
        if not self.name:
            return False
            
        # Action-specific validation
        if self.action_type == ActionType.VARIABLE:
            return bool(self.var_name)
        elif self.action_type == ActionType.POOL:
            return True  # No specific requirements
        elif self.action_type in (ActionType.CALL_ACTION_LIST, ActionType.RUN_ACTION_LIST):
            return bool(self.action_list_name)
        else:
            return True  # Spell actions just need a name

class ActionList:
    """Represents a list of actions in the SimC APL"""
    
    def __init__(self, name: str, preconditions: Optional[str] = None):
        self.name = name
        self.preconditions = preconditions
        self.actions: List[Action] = []
        
    def add_action(self, action: Action):
        """Add an action to this list"""
        self.actions.append(action)
        
    def __str__(self) -> str:
        return f"ActionList({self.name}, actions={len(self.actions)})"
        
    def __repr__(self) -> str:
        return self.__str__()

class ActionParser:
    """Parser for converting SimC actions to PS Lua code"""
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "
        
    def generate_lua(self, actions: List[Action]) -> str:
        """Generate PS Lua code from parsed actions"""
        lua_lines = []
        
        # Add header
        lua_lines.extend([
            "-- Generated by PS SimC Parser",
            "",
            "local PS = ...",
            "local Spell = PS.Spell",
            "local Player = PS.Player",
            "local Target = Player.Target",
            "local Enemies = Player.Enemies",
            "local Cache = {}"
            "",
            "-- Initialize cache",
            "function Cache:Get(key, default)",
            "    return self[key] or default",
            "end",
            "",
            "function Cache:Set(key, value)",
            "    self[key] = value",
            "end",
            "",
            "local Rotation = {",
            "    Name = 'Generated Rotation',",
            "    Profile = 'auto',",
            "    Cache = Cache,",
            "}",
            ""
        ])
        
        # Generate main rotation function
        lua_lines.extend(self._generate_rotation_function(actions))
        
        # Add footer
        lua_lines.extend([
            "",
            "return Rotation"
        ])
        
        return "\n".join(lua_lines)
        
    def _generate_rotation_function(self, actions: List[Action]) -> List[str]:
        """Generate the main rotation function"""
        lines = [
            "function Rotation:Execute()",
            "    -- Check if we have a valid target",
            "    if not Target:Exists() or Target:IsDead() then",
            "        return",
            "    end",
            ""
        ]
        
        # Add each action
        for action in actions:
            lines.extend(self._generate_action(action))
            
        lines.append("end")
        return lines
        
    def _generate_action(self, action: Action) -> List[str]:
        """Generate Lua code for a single action"""
        lines = []
        
        # Add comment if present
        if action.comment:
            lines.append(f"{self.indent_str}-- {action.comment}")
            
        # Handle different action types
        if action.action_type == ActionType.SPELL:
            lines.extend(self._generate_spell_cast(action))
        elif action.action_type == ActionType.VARIABLE:
            lines.extend(self._generate_variable_operation(action))
        elif action.action_type == ActionType.POOL:
            lines.extend(self._generate_pool_resource(action))
        elif action.action_type == ActionType.CALL_ACTION_LIST:
            lines.extend(self._generate_call_action_list(action))
        elif action.action_type == ActionType.RUN_ACTION_LIST:
            lines.extend(self._generate_run_action_list(action))
            
        return lines
        
    def _generate_variable_operation(self, action: Action) -> List[str]:
        """Generate Lua code for variable operations"""
        lines = []
        
        # Add conditions if present
        if action.has_conditions():
            lines.append(f"{self.indent_str}if {self._convert_conditions(action.conditions)} then")
            self.indent_level += 1
            
        # Add the variable operation
        if action.var_name and action.var_value:
            op = action.var_op or 'set'
            if op == 'set':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', {action.var_value})")
            elif op == 'add':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', Cache:Get('{action.var_name}', 0) + {action.var_value})")
            elif op == 'sub':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', Cache:Get('{action.var_name}', 0) - {action.var_value})")
            elif op == 'mul':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', Cache:Get('{action.var_name}', 0) * {action.var_value})")
            elif op == 'div':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', Cache:Get('{action.var_name}', 0) / {action.var_value})")
            elif op == 'max':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', math.max(Cache:Get('{action.var_name}', 0), {action.var_value}))")
            elif op == 'min':
                lines.append(f"{self.indent_str * (self.indent_level + 1)}Cache:Set('{action.var_name}', math.min(Cache:Get('{action.var_name}', 0), {action.var_value}))")
                
        # Close condition if present
        if action.has_conditions():
            self.indent_level -= 1
            lines.append(f"{self.indent_str}end")
            
        return lines
        
    def _generate_spell_cast(self, action: Action) -> List[str]:
        """Generate Lua code for casting a spell"""
        lines = []
        
        # Add conditions if present
        if action.has_conditions():
            lines.append(f"{self.indent_str}if {self._convert_conditions(action.conditions)} then")
            self.indent_level += 1
            
        # Add the spell cast
        spell_name = action.spell_name
        if not spell_name:
            return lines
            
        # Handle different spell cast types
        target = action.args.get('target', '')
        if target == 'ground':
            lines.append(f"{self.indent_str * (self.indent_level + 1)}if Player:Cast(Spell.{spell_name}, 'ground') then")
        else:
            lines.append(f"{self.indent_str * (self.indent_level + 1)}if Player:Cast(Spell.{spell_name}) then")
            
        lines.append(f"{self.indent_str * (self.indent_level + 2)}return true")
        lines.append(f"{self.indent_str * (self.indent_level + 1)}end")
        
        # Close condition if present
        if action.has_conditions():
            self.indent_level -= 1
            lines.append(f"{self.indent_str}end")
            
        return lines
        
    def _generate_pool_resource(self, action: Action) -> List[str]:
        """Generate Lua code for resource pooling"""
        lines = []
        
        if action.pool_for_next:
            lines.append(f"{self.indent_str}if Player.Fury < {action.pool_extra_amount or 0} then")
            lines.append(f"{self.indent_str}    return true")
            lines.append(f"{self.indent_str}end")
            
        return lines
        
    def _generate_call_action_list(self, action: Action) -> List[str]:
        """Generate Lua code for calling another action list"""
        lines = []
        
        if action.has_conditions():
            lines.append(f"{self.indent_str}if {self._convert_conditions(action.conditions)} then")
            self.indent_level += 1
            
        lines.append(f"{self.indent_str * (self.indent_level + 1)}if {action.action_list_name}() then")
        lines.append(f"{self.indent_str * (self.indent_level + 2)}return true")
        lines.append(f"{self.indent_str * (self.indent_level + 1)}end")
        
        if action.has_conditions():
            self.indent_level -= 1
            lines.append(f"{self.indent_str}end")
            
        return lines
        
    def _generate_run_action_list(self, action: Action) -> List[str]:
        """Generate Lua code for running another action list"""
        lines = []
        
        if action.has_conditions():
            lines.append(f"{self.indent_str}if {self._convert_conditions(action.conditions)} then")
            lines.append(f"{self.indent_str}    return {action.action_list_name}()")
            lines.append(f"{self.indent_str}end")
        else:
            lines.append(f"{self.indent_str}return {action.action_list_name}()")
            
        return lines
        
    def _convert_conditions(self, conditions: List[str]) -> str:
        """Convert SimC conditions to Lua conditions"""
        converted = []
        for condition in conditions:
            # Convert SimC operators to Lua
            condition = condition.strip()
            
            # Handle ! operator specially (no space after it)
            condition = re.sub(r'!([^ ])', r'!\1', condition)  # Ensure no space after !
            
            # Add spaces around other operators
            condition = re.sub(r'([<>=]+)', r' \1 ', condition)
            condition = re.sub(r'\s+', ' ', condition)  # Normalize spaces
            
            # Convert comparison operators
            condition = condition.replace('= =', '==')  # Fix double space from above
            condition = condition.replace('>= =', '>=')  # Fix double space from above
            condition = condition.replace('<= =', '<=')  # Fix double space from above
            
            # Convert logical operators
            condition = condition.replace('&&', 'and')
            condition = condition.replace('||', 'or')
            
            converted.append(condition.strip())
            
        return " and ".join(converted)
