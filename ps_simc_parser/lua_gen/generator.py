"""
Lua code generator for PS SimC Parser
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path
from ..api.mapping import (
    logger, monitor, recovery, compatibility,
    convert_spell, convert_condition, convert_resource,
    RESOURCE_MAPPINGS, SpellMapping, ResourceMapping, SPELL_MAPPINGS
)
from ..api.validator import is_valid_condition, is_valid_spell
from ..config import API_VERSION
from .templates import LuaTemplate
import re

class GeneratorError(Exception):
    """Custom exception for generator errors"""
    pass

class LuaGenerator:
    """Generate Lua code from parsed SimC APL"""
    
    def __init__(self):
        self.template = LuaTemplate()
        self.logger = logger
        self.monitor = monitor
        self.recovery = recovery
        self.compatibility = compatibility
        self.context = {}
        self.variables = {}
        self.action_lists = {}
        self._cache = {}
        
    def generate(self, actions: List[Dict], context: Dict) -> str:
        """Generate Lua code from SimC APL."""
        # Validate API version
        compatibility.check_version(API_VERSION)

        # Start performance monitoring
        monitor.start_operation('generate')

        try:
            # Generate Lua code
            lua_code = self.template.render({
                'metadata': self._generate_metadata(context),
                'action_lists': self._generate_action_lists(actions),
                'context': context
            })

            # End performance monitoring
            monitor.end_operation('generate')

            return lua_code

        except Exception as e:
            # Handle errors
            logger.error(f'Error generating Lua code: {e}')
            recovery.handle_error(e)
            raise GeneratorError(str(e))

    def _generate_metadata(self, context: Dict) -> Dict:
        """Generate metadata for the Lua code."""
        metadata = {
            'name': context.get('name', 'Generated Rotation'),
            'profile': context.get('profile', 'auto'),
            'class': context.get('class', 'Unknown'),
            'spec': context.get('spec', 'Unknown'),
            'role': context.get('role', 'dps'),
            'generator': 'PS SimC Parser',
            'version': API_VERSION,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        return metadata

    def _generate_action_lists(self, actions: Union[List[Dict], Dict]) -> Dict[str, str]:
        """Generate Lua code for action lists.
        
        Args:
            actions: Either a list of actions (for single action list) or
                    a dictionary of action lists (for multiple lists)
        
        Returns:
            Dictionary mapping action list names to their Lua code
        """
        action_lists = {}
        
        try:
            # Case 1: Dictionary input (multiple action lists)
            if isinstance(actions, dict):
                for list_name, action_list in actions.items():
                    action_lists[list_name] = self._generate_action_list(action_list)
            # Case 2: List input (single action list)
            elif isinstance(actions, list):
                action_lists['default'] = self._generate_action_list(actions)
            else:
                raise GeneratorError(f'Invalid actions type: {type(actions)}')
                
            return action_lists
            
        except Exception as e:
            raise GeneratorError(f'Failed to generate action lists: {str(e)}')
            
    def _generate_action_list(self, actions: List[Dict]) -> str:
        """Generate Lua code for a single action list."""
        lua_lines = []
        
        # First pass: declare variables
        for action in actions:
            if action['type'] == 'variable':
                var_name = action['name']
                if 'value' in action:
                    lua_lines.append(f'local {var_name} = {action["value"]}')
                    
        # Second pass: handle actions and variable operations
        for action in actions:
            if action['type'] == 'variable':
                var_name = action['name']
                if 'op' in action:
                    op = action['op']
                    if op == 'reset':
                        lua_lines.append(f'{var_name} = {action["value"]}')
                    elif op == 'set':
                        lua_lines.append(f'{var_name} = {action["value"]}')
                    elif op == 'setif':
                        condition = action.get('conditions', [{}])[0]
                        value = action['value']
                        value_else = action.get('value_else', '0')
                        lua_lines.append(f'{var_name} = {condition} and {value} or {value_else}')
                    elif op in ['add', 'sub', 'mul', 'div']:
                        op_map = {'add': '+', 'sub': '-', 'mul': '*', 'div': '/'}
                        lua_lines.append(f'{var_name} = {var_name} {op_map[op]} {action["value"]}')
                    elif op in ['max', 'min']:
                        lua_lines.append(f'{var_name} = math.{op}({var_name}, {action["value"]})')
            elif action['type'] == 'spell':
                # Handle spell casts
                spell_name = action['name']
                if not is_valid_spell(spell_name):
                    raise GeneratorError(f'Invalid spell: {spell_name}')
                    
                spell = convert_spell(spell_name)
                conditions = []
                
                # Add conditions
                if 'conditions' in action:
                    for condition in action['conditions']:
                        if condition:
                            conditions.append(convert_condition(condition))
                            
                # Add arguments as conditions
                if 'args' in action:
                    for key, value in action['args'].items():
                        if key == 'if':
                            conditions.append(convert_condition(value))
                            
                # Generate condition string
                condition_str = ' and '.join(conditions) if conditions else 'true'
                
                # Generate spell cast
                lua_lines.append(f'if {condition_str} then')
                lua_lines.append(f'    return {spell}')
                lua_lines.append('end')
                
        return '\n'.join(lua_lines)

    def _convert_conditions(self, conditions: List[str]) -> str:
        """Convert SimC conditions to Lua conditions."""
        converted = []
        
        for condition in conditions:
            try:
                # Convert condition using API mapping
                converted_condition = convert_condition(condition)
                converted.append(converted_condition)
            except ValueError as e:
                # Handle special cases not covered by convert_condition
                if 'active_enemies' in condition:
                    # Parse active_enemies condition (e.g., "active_enemies>=3")
                    parts = condition.split('active_enemies')
                    if len(parts) == 2:
                        operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                        value = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                        converted.append(f"Enemies:Count() {operator} {value}")
                elif 'soul_fragments' in condition:
                    # Parse soul_fragments condition (e.g., "soul_fragments>=4")
                    parts = condition.split('soul_fragments')
                    if len(parts) == 2:
                        operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                        value = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                        converted.append(f"Player:SoulFragments() {operator} {value}")
                elif 'fury' in condition:
                    # Parse fury condition (e.g., "fury>=60")
                    parts = condition.split('fury')
                    if len(parts) == 2:
                        operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                        value = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                        converted.append(f"Player:Fury() {operator} {value}")
                else:
                    raise GeneratorError(f"Failed to convert condition: {condition}")

        return f"['{' and '.join(converted)}']" if converted else "[]"

    def _generate_variable_action(self, action):
        """Generate Lua code for variable actions."""
        name = action.get('name')
        value = action.get('value')
        
        if not name or not value:
            raise GeneratorError("Variable action missing name or value")
            
        # Convert the value to a Lua condition
        if isinstance(value, str):
            if 'active_enemies' in value:
                # Handle active_enemies conditions
                parts = value.split('active_enemies')
                if len(parts) == 2:
                    operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                    val = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                    lua_value = f"Enemies:Count() {operator} {val}"
            elif 'incoming_damage_5s' in value:
                # Handle incoming damage check
                parts = value.split('incoming_damage_5s')
                if len(parts) == 2:
                    operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                    val = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                    lua_value = f"Player:IncomingDamage(5) {operator} {val}"
            elif 'variable.' in value:
                # Handle variable references
                var_name = value.split('variable.')[1].split('|')[0]  # Handle OR cases
                lua_value = f'Cache:Get("{var_name}")'
            elif '|' in value:
                # Handle OR conditions
                parts = value.split('|')
                conditions = []
                for part in parts:
                    if 'variable.' in part:
                        var_name = part.split('variable.')[1]
                        conditions.append(f'Cache:Get("{var_name}")')
                    elif 'incoming_damage_5s' in part:
                        damage_parts = part.split('>')
                        if len(damage_parts) == 2:
                            conditions.append(f'Player:IncomingDamage(5) > {damage_parts[1]}')
                lua_value = ' or '.join(conditions)
            else:
                lua_value = value
                
        # Generate variable assignment
        return f'    Cache:Set("{name}", {lua_value})\n'

    def _generate_spell_cast(self, action):
        """Generate Lua code for a spell cast action."""
        # Handle both string and dictionary action formats
        if isinstance(action, str):
            # Parse basic spell action format: spell,if=condition
            parts = action.split(',', 1)
            action = {'type': 'spell', 'name': parts[0]}
            if len(parts) > 1:
                # Handle if=condition part
                for param in parts[1].split(','):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        action[key] = value
                
        # Get spell name
        name = action.get('name')
        if not name:
            raise GeneratorError("Missing spell name in action")
        
        # Normalize and look up spell
        name = name.lower()
        try:
            spell_mapping = SPELL_MAPPINGS[name]
            spell = spell_mapping.ps_name
        except KeyError:
            raise GeneratorError(f"Invalid spell: {name}")

        # Parse conditions - only if action is a dictionary
        conditions = []
        if isinstance(action, dict) and 'if' in action:
            # Split on & to handle multiple conditions
            if_conditions = action['if'].split('&')
            conditions.extend([cond.strip() for cond in if_conditions])

        # Convert conditions to Lua format
        condition_parts = []
        if conditions:
            for condition in conditions:
                if 'active_enemies' in condition:
                    # Parse active_enemies condition
                    parts = condition.split('active_enemies')
                    if len(parts) == 2:
                        operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                        value = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                        condition_parts.append(f"Enemies:Count() {operator} {value}")
                elif 'soul_fragments' in condition:
                    # Parse soul_fragments condition
                    parts = condition.split('soul_fragments')
                    if len(parts) == 2:
                        operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                        value = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                        condition_parts.append(f"Player:SoulFragments() {operator} {value}")
                elif 'fury' in condition:
                    # Parse fury condition
                    parts = condition.split('fury')
                    if len(parts) == 2:
                        operator = parts[1][:2] if any(op in parts[1][:2] for op in ['>=', '<=', '==']) else parts[1][0]
                        value = parts[1][2:] if len(operator) == 2 else parts[1][1:]
                        condition_parts.append(f"Player:Fury() {operator} {value}")

        # Generate spell cast code with conditions
        if condition_parts:
            return f"    if Spell.{spell}:IsReady() and {' and '.join(condition_parts)} then\n        return Cast(Spell.{spell})\n    end\n"
        else:
            return f"    if Spell.{spell}:IsReady() then\n        return Cast(Spell.{spell})\n    end\n"

    def _generate_action_list_call(self, action: Dict) -> str:
        """Generate Lua code for an action list call."""
        list_name = action['name']
        conditions = action.get('conditions', [])
        
        # Convert conditions to Lua syntax
        if conditions:
            conditions = [convert_condition(c) for c in conditions]
        
        # Build condition string
        condition_str = ' and '.join(conditions) if conditions else 'true'
        
        return f"""if {condition_str} then
    return Rotation:{list_name}()
end"""
        
    def _generate_imports(self) -> str:
        """Generate PS API imports"""
        imports = [
            'PS',
            'Spell',
            'Player',
            'Target',
            'Enemies',
            'Unit',
            'Item',
            'MultiUnits',
            'Combat',
        ]
        
        if self.context.get('use_mechanics', False):
            imports.extend([
                'Mechanics',
                'Position',
                'Movement',
            ])
            
        return self.template.format_imports(imports)
        
    def _generate_variables(self) -> str:
        """Generate variable declarations"""
        variables = []
        
        # Add state variables
        variables.extend([
            self.template.format_variable_declaration('Cache', '{}'),
            self.template.format_variable_declaration('LastCast', '0'),
            self.template.format_variable_declaration('LastGCD', '0'),
            self.template.format_variable_declaration('LastOffGCD', '0'),
            self.template.format_variable_declaration('CombatTime', '0'),
            self.template.format_variable_declaration('TargetGUID', 'nil'),
        ])
        
        # Add custom variables
        for name, value in self.variables.items():
            variables.append(
                self.template.format_variable_declaration(name, value)
            )
            
        return '\n'.join(variables)
        
    def _generate_rotation(self) -> str:
        """Generate rotation table"""
        return self.template.format_rotation(
            name=self.context.get('name', 'Generated Rotation'),
            profile=self.context.get('profile', 'auto'),
            class_name=self.context.get('class', 'Unknown'),
            spec=self.context.get('spec', 'Unknown'),
            role=self.context.get('role', 'Unknown'),
        )
        
    def _generate_utility_functions(self) -> str:
        """Generate utility functions"""
        functions = []
        
        # Add core utility functions
        functions.append(self.template.format_utility_functions())
        
        # Add mechanic functions if needed
        if self.context.get('use_mechanics', False):
            functions.append(self._generate_mechanic_functions())
            
        # Add custom utility functions
        for name, body in self.context.get('custom_functions', {}).items():
            functions.append(
                self.template.format_function(name, body=body)
            )
            
        return '\n'.join(functions)
        
    def _generate_mechanic_functions(self) -> str:
        """Generate mechanic-specific functions"""
        return """
function Rotation:HandleMechanics()
    -- Handle movement
    if Player:IsMoving() then
        return self:HandleMovement()
    end
    
    -- Handle positioning
    if not self:IsInPosition() then
        return self:HandlePositioning()
    end
    
    -- Handle mechanics
    local mechanic = Mechanics:GetActiveMechanic()
    if mechanic then
        return self:HandleMechanic(mechanic)
    end
end

function Rotation:IsInPosition()
    -- Check if we're in the correct position
    return Position:IsValid()
end

function Rotation:HandleMovement()
    -- Handle movement abilities
    for _, spell in ipairs(self.MovementSpells) do
        if spell:IsReady() then
            return Cast(spell)
        end
    end
end

function Rotation:HandlePositioning()
    -- Get to the correct position
    local position = Position:GetOptimal()
    if position then
        return Movement:MoveTo(position)
    end
end

function Rotation:HandleMechanic(mechanic)
    -- Handle specific mechanics
    if self.MechanicHandlers[mechanic] then
        return self.MechanicHandlers[mechanic](self)
    end
end
"""
        
    def _combine_sections(self, sections: Dict[str, str]) -> str:
        """Combine code sections"""
        return '\n\n'.join(filter(None, sections.values()))
        
    def _validate_lua_code(self, code: str) -> None:
        """Validate generated Lua code"""
        # TODO: Add Lua syntax validation
        pass
        
    def save(self, code: str, output_path: str) -> None:
        """Save generated code to file"""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(code)
            self.logger.info(f"Saved Lua code to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving file: {str(e)}")
            raise 