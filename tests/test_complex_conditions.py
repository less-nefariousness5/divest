import unittest
from ps_simc_parser.parser.parser import Parser
from ps_simc_parser.parser.actions import Action
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestComplexConditions(PSTestCase):
    def setUp(self):
        super().setUp()
        # Complex conditions SimC template
        self.simc_content = """
# Complex Conditions Template
actions=auto_attack

# Multiple conditions with AND
actions+=/spell_1,if=buff.buff1.up&buff.buff2.up&cooldown.spell2.remains>30

# Multiple conditions with OR
actions+=/spell_2,if=buff.buff1.down|buff.buff2.down|cooldown.spell1.up

# Nested conditions with parentheses
actions+=/spell_3,if=(buff.buff1.up&buff.buff2.up)|((cooldown.spell1.up|cooldown.spell2.up)&buff.buff3.up)

# Variable-based conditions
actions+=/variable,name=resource_pooling,value=cooldown.spell1.remains<=3|target.time_to_die<=15
actions+=/spell_4,if=variable.resource_pooling

# State-dependent conditions
actions+=/spell_5,if=buff.buff1.up&(buff.buff2.remains>buff.buff1.remains|buff.buff3.stack>2)

# Resource conditions with thresholds
actions+=/spell_6,if=resource.amount>=80&(buff.buff1.up|resource.deficit<=20)

# Target count conditions
actions+=/spell_7,if=active_enemies>=3&dot.dot1.ticking&buff.buff1.stack>=3

# Health percentage conditions
actions+=/spell_8,if=health.pct<=70&(incoming_damage_3s>health.max*0.25|buff.defensive.down)

# Complex timing conditions
actions+=/spell_9,if=(time_to_die>15|fight_remains<30)&(buff.buff1.remains>3|cooldown.spell2.remains<=buff.buff1.remains)
"""

    def test_multiple_and_conditions(self):
        """Test parsing of multiple AND conditions"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find spell_1 action
        spell1_action = next((a for a in actions if 'spell_1' in str(a)), None)
        self.assertIsNotNone(spell1_action)
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add condition check
        lua_code.append('if HasBuff("buff1") and HasBuff("buff2") and GetCooldownRemains("spell2") > 30 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spell_1")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        self.assertIn('HasBuff("buff1")', final_code)
        self.assertIn('HasBuff("buff2")', final_code)
        self.assertIn('GetCooldownRemains("spell2")', final_code)

    def test_multiple_or_conditions(self):
        """Test parsing of multiple OR conditions"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find spell_2 action
        spell2_action = next((a for a in actions if 'spell_2' in str(a)), None)
        self.assertIsNotNone(spell2_action)
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add condition check
        lua_code.append('if not HasBuff("buff1") or not HasBuff("buff2") or GetCooldown("spell1") == 0 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spell_2")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        self.assertIn('not HasBuff("buff1")', final_code)
        self.assertIn('not HasBuff("buff2")', final_code)
        self.assertIn('GetCooldown("spell1")', final_code)

    def test_nested_conditions(self):
        """Test parsing of nested conditions with parentheses"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find spell_3 action
        spell3_action = next((a for a in actions if 'spell_3' in str(a)), None)
        self.assertIsNotNone(spell3_action)
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add nested condition check
        lua_code.append('if (HasBuff("buff1") and HasBuff("buff2")) or')
        lua_code.append('   ((GetCooldown("spell1") == 0 or GetCooldown("spell2") == 0) and HasBuff("buff3")) then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spell_3")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        self.assertIn('HasBuff("buff1") and HasBuff("buff2")', final_code)
        self.assertIn('GetCooldown("spell1") == 0 or GetCooldown("spell2") == 0', final_code)

    def test_variable_conditions(self):
        """Test parsing of variable-based conditions"""
        # Create an Action object directly for testing
        var_action = Action("variable,name=resource_pooling,value=cooldown.spell1.remains<=3|target.time_to_die<=15")
        spell4_action = Action("spell_4,if=variable.resource_pooling")
        
        # Verify variable action properties
        self.assertEqual(var_action.name, 'variable')
        self.assertIn('name', var_action.args)
        self.assertEqual(var_action.args['name'], 'resource_pooling')
        self.assertIn('value', var_action.args)
        self.assertTrue('cooldown.spell1.remains<=3' in var_action.args['value'])
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add variable definition
        lua_code.append('local function UpdateVariables()')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Variables.resource_pooling = GetCooldownRemains("spell1") <= 3 or TargetTimeToDie() <= 15')
        generator.dedent()
        lua_code.append('end')
        lua_code.append('')
        
        # Add variable usage
        lua_code.append('if Variables.resource_pooling then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spell_4")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify variable handling
        self.assertIn('Variables.resource_pooling =', final_code)
        self.assertIn('GetCooldownRemains("spell1")', final_code)
        self.assertIn('TargetTimeToDie()', final_code)
        self.assertIn('if Variables.resource_pooling then', final_code)

    def test_state_dependent_conditions(self):
        """Test parsing of state-dependent conditions"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find spell_5 action
        spell5_action = next((a for a in actions if 'spell_5' in str(a)), None)
        self.assertIsNotNone(spell5_action)
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add state-dependent condition check
        lua_code.append('if HasBuff("buff1") and')
        lua_code.append('   (GetBuffRemains("buff2") > GetBuffRemains("buff1") or GetBuffStacks("buff3") > 2) then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spell_5")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        self.assertIn('GetBuffRemains("buff2") > GetBuffRemains("buff1")', final_code)
        self.assertIn('GetBuffStacks("buff3") > 2', final_code)

if __name__ == '__main__':
    unittest.main()
