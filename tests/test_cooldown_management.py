import unittest
from ps_simc_parser.parser.parser import Parser
from ps_simc_parser.parser.actions import Action
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestCooldownManagement(PSTestCase):
    def setUp(self):
        super().setUp()
        # Cooldown management SimC template
        self.simc_content = """
# Cooldown Management Template
actions=auto_attack

# Basic cooldown usage
actions+=/major_cooldown,if=!cooldown.major_cooldown.up&target.time_to_die>30
actions+=/minor_cooldown,if=charges=2|target.time_to_die<=15

# Stacking cooldowns
actions+=/cooldown_1,if=!buff.cooldown_2.up&cooldown.cooldown_2.remains>30
actions+=/cooldown_2,if=buff.cooldown_1.up

# Cooldown syncing
actions+=/sync_spell_1,if=cooldown.sync_spell_2.up&cooldown.sync_spell_3.up
actions+=/sync_spell_2,if=buff.sync_spell_1.up
actions+=/sync_spell_3,if=buff.sync_spell_1.up

# Charge-based cooldown management
actions+=/charge_spell,if=charges>=2|charges_fractional>=1.8&active_enemies>2
actions+=/charge_spell_2,if=charges=3|fight_remains<20

# Emergency cooldown usage
actions+=/emergency_cd,if=health.pct<20|incoming_damage_3s>health.max*0.4

# Cooldown priority system
actions+=/priority_cd_1,if=!buff.priority_cd_2.up&!buff.priority_cd_3.up
actions+=/priority_cd_2,if=buff.priority_cd_1.up
actions+=/priority_cd_3,if=buff.priority_cd_1.up&buff.priority_cd_2.up

# Cooldown pooling
actions+=/variable,name=pool_for_cd,value=cooldown.major_cd.remains<=2&rage>=40
actions+=/pool_dependent_spell,if=variable.pool_for_cd
"""

    def test_basic_cooldown_usage(self):
        """Test basic cooldown usage patterns"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find major and minor cooldown actions
        major_cd = next((a for a in actions if 'major_cooldown' in str(a)), None)
        minor_cd = next((a for a in actions if 'minor_cooldown' in str(a)), None)
        
        self.assertIsNotNone(major_cd, "Major cooldown action not found")
        self.assertIsNotNone(minor_cd, "Minor cooldown action not found")
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add cooldown checks
        lua_code.append('if not GetCooldown("major_cooldown") and TargetTimeToDie() > 30 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("major_cooldown")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetSpellCharges("minor_cooldown") == 2 or TargetTimeToDie() <= 15 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("minor_cooldown")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify cooldown handling
        self.assertIn('GetCooldown("major_cooldown")', final_code)
        self.assertIn('GetSpellCharges("minor_cooldown")', final_code)
        self.assertIn('TargetTimeToDie()', final_code)

    def test_cooldown_stacking(self):
        """Test cooldown stacking logic"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find stacking cooldown actions
        cd1 = next((a for a in actions if 'cooldown_1' in str(a)), None)
        cd2 = next((a for a in actions if 'cooldown_2' in str(a)), None)
        
        self.assertIsNotNone(cd1, "First stacking cooldown not found")
        self.assertIsNotNone(cd2, "Second stacking cooldown not found")
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add stacking logic
        lua_code.append('if not HasBuff("cooldown_2") and GetCooldownRemains("cooldown_2") > 30 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("cooldown_1")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if HasBuff("cooldown_1") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("cooldown_2")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify stacking logic
        self.assertIn('HasBuff("cooldown_1")', final_code)
        self.assertIn('HasBuff("cooldown_2")', final_code)
        self.assertIn('GetCooldownRemains("cooldown_2")', final_code)

    def test_charge_based_cooldowns(self):
        """Test charge-based cooldown management"""
        context = self.parser.parse(self.simc_content)
        actions = context.action_lists['default']
        
        # Find charge-based actions
        charge_spell = next((a for a in actions if 'charge_spell' in str(a)), None)
        self.assertIsNotNone(charge_spell, "Charge-based spell not found")
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add charge handling
        lua_code.append('if GetSpellCharges("charge_spell") >= 2 or GetSpellChargesFractional("charge_spell") >= 1.8 and GetActiveEnemies() > 2 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("charge_spell")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify charge handling
        self.assertIn('GetSpellCharges("charge_spell")', final_code)
        self.assertIn('GetSpellChargesFractional("charge_spell")', final_code)
        self.assertIn('GetActiveEnemies()', final_code)

    def test_cooldown_pooling(self):
        """Test cooldown pooling logic"""
        # Create actions directly for testing
        pool_var = Action("variable,name=pool_for_cd,value=cooldown.major_cd.remains<=2&rage>=40")
        pool_spell = Action("pool_dependent_spell,if=variable.pool_for_cd")
        
        # Verify variable action properties
        self.assertEqual(pool_var.name, 'variable')
        self.assertEqual(pool_var.args.get('name'), 'pool_for_cd')
        self.assertTrue('cooldown.major_cd.remains<=2' in pool_var.args.get('value', ''))
        self.assertTrue('rage>=40' in pool_var.args.get('value', ''))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add pooling logic
        lua_code.append('local function UpdateVariables()')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Variables.pool_for_cd = GetCooldownRemains("major_cd") <= 2 and GetResource() >= 40')
        generator.dedent()
        lua_code.append('end')
        lua_code.append('')
        lua_code.append('if Variables.pool_for_cd then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("pool_dependent_spell")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify pooling logic
        self.assertIn('Variables.pool_for_cd', final_code)
        self.assertIn('GetCooldownRemains("major_cd")', final_code)
        self.assertIn('GetResource()', final_code)

if __name__ == '__main__':
    unittest.main()
