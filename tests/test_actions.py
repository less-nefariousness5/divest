"""Test action parser functionality."""

import unittest
from ps_simc_parser.parser.actions import ActionParser
from ps_simc_parser.parser.apl import Action

class TestActionParser(unittest.TestCase):
    """Test action parser functionality."""
    
    def setUp(self):
        """Set up test cases."""
        self.parser = ActionParser()
        
    def test_generate_simple_action(self):
        """Test generating Lua code for a simple action."""
        actions = [Action(
            name="immolation_aura",
            conditions=[],
            args={}
        )]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("function Rotation:Execute()", lua_code)
        self.assertIn("local Player = PS.Player", lua_code)
        self.assertIn("local Target = Player.Target", lua_code)
        self.assertIn("local Spells = PS.Spells", lua_code)
        self.assertIn("if Player:Cast(Spells.ImmolationAura) then", lua_code)
        
    def test_generate_action_with_condition(self):
        """Test generating Lua code for an action with conditions."""
        actions = [Action(
            name="spirit_bomb",
            conditions=["soul_fragments>=4"],
            args={}
        )]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if Player.SoulFragments >= 4 then", lua_code)
        self.assertIn("if Player:Cast(Spells.SpiritBomb) then", lua_code)
        
    def test_generate_action_with_args(self):
        """Test generating Lua code for an action with arguments."""
        actions = [Action(
            name="sigil_of_flame",
            conditions=["!debuff.sigil_of_flame.up"],
            args={"target": "ground"}
        )]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if not Target.Debuff(Spells.SigilOfFlame).Exists then", lua_code)
        self.assertIn("if Player:Cast(Spells.SigilOfFlame, 'ground') then", lua_code)
        
    def test_generate_multiple_actions(self):
        """Test generating Lua code for multiple actions."""
        actions = [
            Action(name="immolation_aura", conditions=[], args={}),
            Action(name="spirit_bomb", conditions=["soul_fragments>=4"], args={}),
            Action(name="sigil_of_flame", conditions=["!debuff.sigil_of_flame.up"], args={"target": "ground"})
        ]
        
        lua_code = self.parser.generate_lua(actions)
        # Check order of actions
        immolation_pos = lua_code.find("ImmolationAura")
        spirit_bomb_pos = lua_code.find("SpiritBomb")
        sigil_pos = lua_code.find("SigilOfFlame")
        
        self.assertLess(immolation_pos, spirit_bomb_pos)
        self.assertLess(spirit_bomb_pos, sigil_pos)
        
    def test_generate_variable(self):
        """Test generating Lua code for variable definitions."""
        actions = [Action(
            name="variable",
            conditions=[],
            args={
                "name": "brand_build",
                "value": "talent.burning_brand.enabled"
            }
        )]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("local brand_build = Player.Talent(Spells.BurningBrand).Enabled", lua_code)
        
    def test_generate_complex_conditions(self):
        """Test generating Lua code for complex conditions."""
        actions = [Action(
            name="fel_devastation",
            conditions=[
                "!buff.metamorphosis.up",
                "fury>=50",
                "incoming_damage_5s>0"
            ],
            args={}
        )]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if not Player.Buff(Spells.Metamorphosis).Exists and Player.Fury >= 50 and Player:IncomingDamage(5) > 0 then", lua_code)
        self.assertIn("if Player:Cast(Spells.FelDevastation) then", lua_code)
