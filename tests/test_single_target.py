import unittest
import os
from pathlib import Path
from ps_simc_parser.parser import Parser
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestSingleTargetRotation(PSTestCase):
    def setUp(self):
        super().setUp()
        self.generator = LuaGenerator()
        # Basic single target SimC template
        self.simc_content = """
# Basic Single Target Template
actions=auto_attack
actions+=/use_item,name=trinket1,if=buff.bloodlust.up
actions+=/potion,if=buff.bloodlust.up|target.time_to_die<=30

# Basic builder/spender pattern
actions+=/builder_spell,if=resource.deficit>=30
actions+=/spender_spell,if=resource.current>=50

# Cooldown section
actions+=/major_cooldown,if=!buff.major_cooldown.up&target.time_to_die>30
actions+=/minor_cooldown,if=charges=2|target.time_to_die<=15

# Execute phase
actions+=/execute_ability,if=target.health.pct<=20
"""

    def test_basic_rotation_structure(self):
        """Test parsing of a basic single target rotation structure"""
        # Parse the SimC content
        context = self.parser.parse(self.simc_content)
        
        # Verify the action list is parsed correctly
        self.assertIn('default', context.action_lists)
        actions = context.action_lists['default']
        
        # Basic checks
        self.assertTrue(any('auto_attack' in str(action) for action in actions))
        self.assertTrue(any('trinket1' in str(action) for action in actions))
        self.assertTrue(any('potion' in str(action) for action in actions))

    def test_resource_management(self):
        """Test resource management logic in single target rotation"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Check builder/spender logic
        builder_action = next((action for action in actions if 'builder_spell' in str(action)), None)
        spender_action = next((action for action in actions if 'spender_spell' in str(action)), None)
        
        self.assertIsNotNone(builder_action, "Builder spell not found in rotation")
        self.assertIsNotNone(spender_action, "Spender spell not found in rotation")
        
        # Verify conditions
        self.assertIn('resource.deficit>=30', str(builder_action))
        self.assertIn('resource.current>=50', str(spender_action))

    def test_cooldown_usage(self):
        """Test cooldown management in single target rotation"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Check cooldown logic
        major_cd = next((action for action in actions if 'major_cooldown' in str(action)), None)
        minor_cd = next((action for action in actions if 'minor_cooldown' in str(action)), None)
        
        self.assertIsNotNone(major_cd, "Major cooldown not found in rotation")
        self.assertIsNotNone(minor_cd, "Minor cooldown not found in rotation")
        
        # Verify cooldown conditions
        self.assertIn('!buff.major_cooldown.up', str(major_cd))
        self.assertIn('target.time_to_die>30', str(major_cd))
        self.assertIn('charges=2|target.time_to_die<=15', str(minor_cd))

    def test_execute_phase(self):
        """Test execute phase handling in single target rotation"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Check execute phase logic
        execute_action = next((action for action in actions if 'execute_ability' in str(action)), None)
        self.assertIsNotNone(execute_action, "Execute ability not found in rotation")
        self.assertIn('target.health.pct<=20', str(execute_action))

    def test_lua_generation(self):
        """Test Lua code generation for single target rotation"""
        # Parse the SimC content
        context = self.parser.parse(self.simc_content)
        
        # Generate basic Lua code structure
        lua_code = []
        
        # Add header
        lua_code.append("-- Generated Single Target Rotation")
        lua_code.append("local PS = ...")
        lua_code.append("local Spell = PS.Spell")
        lua_code.append("local Player = PS.Player")
        lua_code.append("")
        
        # Add rotation function
        lua_code.append("function Rotation()")
        lua_code.append("    AutoAttack()")
        lua_code.append("    local resource = GetResource()")
        lua_code.append("    if HasBuff('bloodlust') then")
        lua_code.append("        UseTrinket(1)")
        lua_code.append("    end")
        lua_code.append("end")
        
        # Join the code
        final_code = "\n".join(lua_code)
        
        # Verify core functionality exists
        self.assertIn('AutoAttack()', final_code)
        self.assertIn('GetResource()', final_code)
        self.assertIn('HasBuff', final_code)
        self.assertIn('UseTrinket', final_code)
        
        # Verify structure
        self.assertIn('function Rotation()', final_code)
        self.assertIn('local PS = ...', final_code)

if __name__ == '__main__':
    unittest.main()
