"""
Lua code generator for PS SimC Parser
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path
import re
import logging

from ..api.mapping import (
    convert_spell, convert_condition, convert_resource,
    RESOURCE_MAPPINGS, SpellMapping, ResourceMapping, SPELL_MAPPINGS
)
from ..api.validator import is_valid_condition, is_valid_spell
from ..config import API_VERSION
from ..utils.compatibility import compatibility
from ..utils.monitor import monitor
from ..utils.recovery import recovery
from .templates import LuaTemplate

# Set up logging
logger = logging.getLogger(__name__)

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
        """Generate Lua code from SimC APL.
        
        Args:
            actions: List of action dictionaries
            context: Context dictionary containing metadata
            
        Returns:
            Generated Lua code
            
        Raises:
            GeneratorError: If code generation fails
        """
        try:
            # Generate metadata
            metadata = self._generate_metadata(context.get('metadata', {}))
            
            # Generate action lists
            action_lists = self._generate_action_lists(actions)
            
            # Render template
            return self.template.render({
                'metadata': metadata,
                'action_lists': action_lists
            })
            
        except (ValueError, KeyError) as e:
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
        """Generate action lists from SimC APL.
        
        Args:
            actions: Either a list of actions (for single action list) or
                    a dictionary of action lists (for multiple lists)
                    
        Returns:
            Dictionary mapping action list names to Lua code
            
        Raises:
            GeneratorError: If action list generation fails
        """
        try:
            # Handle single action list
            if isinstance(actions, list):
                return {'main': self._generate_action_list(actions)}
                
            # Handle multiple action lists
            elif isinstance(actions, dict):
                result = {}
                for name, action_list in actions.items():
                    result[name] = self._generate_action_list(action_list)
                return result
                
            else:
                raise GeneratorError(f"Invalid actions type: {type(actions)}")
                
        except GeneratorError as e:
            raise GeneratorError(f"Failed to generate action lists: {e}")
            
        except Exception as e:
            raise GeneratorError(f"Failed to generate action lists: {e}")

    def _generate_action_list(self, actions: List[Dict]) -> str:
        """Generate a single action list."""
        lua_code = []
        
        for action in actions:
            action_type = action.get('type')
            if action_type == 'spell':
                spell_name = action.get('action')
                if not spell_name:
                    raise GeneratorError("Missing spell name")
                    
                try:
                    spell = convert_spell(spell_name)
                except ValueError as e:
                    raise GeneratorError(f"Unknown spell: {spell_name}")
                
                conditions = action.get('conditions', [])
                lua_conditions = []
                
                for condition in conditions:
                    try:
                        lua_condition = self._convert_condition(condition)
                        lua_conditions.append(lua_condition)
                    except ValueError as e:
                        raise GeneratorError(f"Failed to convert condition: {condition}")
                
                if lua_conditions:
                    condition_str = ' and '.join(lua_conditions)
                    lua_code.append(f"if {condition_str} then")
                
                lua_code.append(f"    if Spell.{spell.ps_name}:IsReady() then")
                if spell_name == 'sigil_of_flame':
                    lua_code.append(f"        return Cast(Spell.{spell.ps_name}, 'ground')")
                else:
                    lua_code.append(f"        return Cast(Spell.{spell.ps_name})")
                lua_code.append("    end")
                
                if lua_conditions:
                    lua_code.append("end")
            
            elif action_type == 'variable':
                lua_code.append(self._generate_variable_action(action))
                
            else:
                raise GeneratorError(f"Unknown action type: {action_type}")
        
        return '\n'.join(lua_code)

    def _convert_condition(self, condition: str) -> str:
        """Convert a SimC condition to Lua code.
        
        Args:
            condition: SimC condition string
            
        Returns:
            Lua condition string
            
        Raises:
            ValueError: If condition cannot be converted
        """
        if not condition or condition.isspace():
            raise ValueError(f"Invalid condition: {condition}")
            
        # First handle variables/functions
        var_mappings = {
            'soul_fragments': 'Player.SoulFragments',
            'buff.metamorphosis.up': 'Player:BuffUp(Spell.Metamorphosis)',
            'target.time_to_die': 'Target.TimeToDie',
            'debuff.sigil_of_flame.up': 'Target:DebuffUp(Spell.SigilOfFlame)',
        }
        
        result = condition
        
        # 1. Handle negation first
        result = result.replace('!', 'not ')
        
        # 2. Replace variables
        for simc_var, lua_var in var_mappings.items():
            result = result.replace(simc_var, lua_var)
        
        # 3. Handle operators
        # First normalize all operators by adding spaces
        result = re.sub(r'([<>=!]+)', r' \1 ', result)
        result = re.sub(r'\s+', ' ', result).strip()
        
        # Now handle each operator while preserving spaces
        result = result.replace(' >= ', ' >= ')  # Keep spaces
        result = result.replace(' <= ', ' <= ')  # Keep spaces
        result = result.replace(' > ', ' > ')    # Keep spaces
        result = result.replace(' < ', ' < ')    # Keep spaces
        result = result.replace(' = ', ' == ')   # Convert = to ==
        result = result.replace(' ! ', ' != ')   # Convert ! to !=
        
        # 4. Handle special cases
        result = result.replace('not ==', '~=')
        result = result.replace('not =', '~=')
        result = result.replace('not not', '')
        
        # 5. Clean up spaces
        parts = []
        for part in result.split():
            if part in ('and', 'or', 'not'):
                parts.append(part)
            else:
                parts.append(part)
        
        # Join with spaces
        result = ' '.join(parts)
        
        # 6. Validate result
        if not result or result.isspace():
            raise ValueError(f"Failed to convert condition: {condition}")
            
        return result

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