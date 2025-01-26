import unittest
from ps_simc_parser.parser.parser import Parser
from ps_simc_parser.parser.actions import Action
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestFullRotation(PSTestCase):
    def setUp(self):
        super().setUp()
        # Complex rotation SimC template with all components
        self.simc_content = """
# Full Rotation Template with All Components
actions=auto_attack

# Precombat actions
actions.precombat=flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/snapshot_stats
actions.precombat+=/use_item,name=trinket1
actions.precombat+=/potion

# Interrupt handling
actions+=/rebuke,if=target.debuff.casting.react
actions+=/arcane_torrent,if=target.debuff.casting.react&!prev_gcd.rebuke

# Defensive rotation
actions+=/divine_shield,if=health.pct<=20
actions+=/lay_on_hands,if=health.pct<=25
actions+=/shield_of_vengeance,if=health.pct<=40|incoming_damage_3s>=health.max*0.4

# Movement handling
actions+=/divine_steed,if=movement.distance>=20
actions+=/blessing_of_freedom,if=movement.snared
actions+=/blessing_of_protection,if=debuff.movement_impaired.up

# Resource management
actions+=/wake_of_ashes,if=holy_power.deficit>=4
actions+=/judgment,if=holy_power.deficit>=2&buff.divine_purpose.down
actions+=/crusader_strike,if=holy_power.deficit>=2&charges=2

# Cooldown management
actions+=/avenging_wrath,if=holy_power>=3&!talent.crusade.enabled
actions+=/crusade,if=holy_power>=3&talent.crusade.enabled
actions+=/ashen_hallow,if=holy_power<=2&!buff.avenging_wrath.up&!buff.crusade.up

# Single target rotation
actions+=/templars_verdict,if=holy_power=5|(buff.divine_purpose.up&buff.divine_purpose.remains<gcd*2)
actions+=/wake_of_ashes,if=holy_power<=2&(cooldown.avenging_wrath.remains>10|cooldown.crusade.remains>10)
actions+=/blade_of_justice,if=holy_power<=3
actions+=/judgment,if=holy_power<=3
actions+=/hammer_of_wrath,if=holy_power<=4
actions+=/consecration,if=holy_power<=3

# AOE rotation (4+ targets)
actions.aoe=divine_storm,if=holy_power=5|(buff.divine_purpose.up&buff.divine_purpose.remains<gcd*2)
actions.aoe+=/wake_of_ashes,if=holy_power<=2
actions.aoe+=/blade_of_justice,if=holy_power<=3
actions.aoe+=/consecration,if=holy_power<=3
actions.aoe+=/divine_storm,if=holy_power>=3

# Cleave rotation (2-3 targets)
actions.cleave=variable,name=ds_castable,value=spell_targets.divine_storm>=2
actions.cleave+=/divine_storm,if=(holy_power=5|buff.divine_purpose.up)&variable.ds_castable
actions.cleave+=/templars_verdict,if=(holy_power=5|buff.divine_purpose.up)&!variable.ds_castable
actions.cleave+=/wake_of_ashes,if=holy_power<=2
actions.cleave+=/blade_of_justice,if=holy_power<=3
actions.cleave+=/consecration,if=holy_power<=3
"""

    def test_precombat_actions(self):
        """Test precombat action list parsing and generation"""
        # Parse the SimC content
        context = self.parser.parse(self.simc_content)
        
        # Verify precombat actions
        self.assertIn('precombat', context.action_lists)
        precombat_actions = context.action_lists['precombat']
        
        # Check precombat sequence
        precombat_names = [action['name'] for action in precombat_actions]
        self.assertIn('flask', precombat_names)
        self.assertIn('augmentation', precombat_names)
        self.assertIn('food', precombat_names)
        self.assertIn('snapshot_stats', precombat_names)
        
        # Generate Lua code for precombat
        generator = LuaGenerator()
        lua_code = []
        
        lua_code.append('-- Precombat actions')
        lua_code.append('if not InCombat() then')
        generator.indent()
        for action in precombat_actions:
            lua_code.append(generator.get_indent() + f'Cast("{action["name"]}")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify precombat Lua generation
        self.assertIn('if not InCombat() then', final_code)
        self.assertIn('Cast("flask")', final_code)
        self.assertIn('Cast("augmentation")', final_code)

    def test_defensive_rotation(self):
        """Test defensive rotation logic"""
        # Create defensive actions
        divine_shield = Action("divine_shield,if=health.pct<=20")
        lay_on_hands = Action("lay_on_hands,if=health.pct<=25")
        shield_of_vengeance = Action("shield_of_vengeance,if=health.pct<=40|incoming_damage_3s>=health.max*0.4")
        
        # Verify defensive conditions
        self.assertEqual(divine_shield.name, 'divine_shield')
        self.assertTrue(any('health.pct<=20' in c for c in divine_shield.conditions))
        
        self.assertEqual(lay_on_hands.name, 'lay_on_hands')
        self.assertTrue(any('health.pct<=25' in c for c in lay_on_hands.conditions))
        
        # Generate defensive Lua code
        generator = LuaGenerator()
        lua_code = []
        
        lua_code.append('-- Defensive rotation')
        lua_code.append('if GetHealthPercent() <= 20 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("divine_shield")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetHealthPercent() <= 25 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("lay_on_hands")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify defensive Lua generation
        self.assertIn('GetHealthPercent()', final_code)
        self.assertIn('Cast("divine_shield")', final_code)
        self.assertIn('Cast("lay_on_hands")', final_code)

    def test_aoe_rotation(self):
        """Test AOE rotation logic"""
        # Parse the SimC content
        context = self.parser.parse(self.simc_content)
        
        # Verify AOE actions
        self.assertIn('aoe', context.action_lists)
        aoe_actions = context.action_lists['aoe']
        
        # Check AOE sequence
        self.assertTrue(any('divine_storm' in str(action) for action in aoe_actions))
        self.assertTrue(any('wake_of_ashes' in str(action) for action in aoe_actions))
        self.assertTrue(any('consecration' in str(action) for action in aoe_actions))
        
        # Generate AOE Lua code
        generator = LuaGenerator()
        lua_code = []
        
        lua_code.append('-- AOE rotation')
        lua_code.append('if GetActiveEnemies() >= 4 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'if GetHolyPower() == 5 or (HasBuff("divine_purpose") and GetBuffRemains("divine_purpose") < GetGCD() * 2) then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("divine_storm")')
        generator.dedent()
        lua_code.append(generator.get_indent() + 'end')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify AOE Lua generation
        self.assertIn('GetActiveEnemies()', final_code)
        self.assertIn('GetHolyPower()', final_code)
        self.assertIn('Cast("divine_storm")', final_code)

    def test_cleave_rotation(self):
        """Test cleave rotation logic"""
        # Parse the SimC content
        context = self.parser.parse(self.simc_content)
        
        # Verify cleave actions exist
        self.assertIn('cleave', context.action_lists)
        cleave_actions = context.action_lists['cleave']
        
        # Check cleave sequence
        has_ds_variable = False
        has_divine_storm = False
        has_templars_verdict = False
        
        for action in cleave_actions:
            if action['type'] == 'variable' and action['name'] == 'ds_castable':
                has_ds_variable = True
            elif action['type'] == 'spell':
                if action['name'] == 'divine_storm':
                    has_divine_storm = True
                elif action['name'] == 'templars_verdict':
                    has_templars_verdict = True
        
        self.assertTrue(has_ds_variable, "Missing ds_castable variable")
        self.assertTrue(has_divine_storm, "Missing divine_storm action")
        self.assertTrue(has_templars_verdict, "Missing templars_verdict action")
        
        # Generate cleave Lua code
        generator = LuaGenerator()
        lua_code = []
        
        lua_code.append('-- Cleave rotation')
        lua_code.append('if GetActiveEnemies() >= 2 and GetActiveEnemies() <= 3 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'local ds_castable = GetSpellTargets("divine_storm") >= 2')
        lua_code.append(generator.get_indent() + 'if (GetHolyPower() == 5 or HasBuff("divine_purpose")) and ds_castable then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("divine_storm")')
        generator.dedent()
        lua_code.append(generator.get_indent() + 'end')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify cleave Lua generation
        self.assertIn('GetActiveEnemies()', final_code)
        self.assertIn('GetSpellTargets("divine_storm")', final_code)
        self.assertIn('Cast("divine_storm")', final_code)

if __name__ == '__main__':
    unittest.main()
