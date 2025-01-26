import unittest
import os
from pathlib import Path
from ps_simc_parser.parser import Parser
from ps_simc_parser.lua_gen import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestVDHIntegration(PSTestCase):
    def setUp(self):
        super().setUp()
        # Load VDH SimC file
        self.simc_file = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / 'vdh.simc'
        with open(self.simc_file, 'r') as f:
            self.simc_content = f.read()
        # Set the specialization for VDH
        self.parser.spec = 'vengeance'

    def test_base_rotation_parsing(self):
        """Test parsing of the base VDH rotation"""
        # Parse the SimC content
        context = self.parser.parse(self.simc_content)
        
        # Verify core action lists are present
        self.assertIn('precombat', context.action_lists)
        self.assertIn('default', context.action_lists)
        self.assertIn('ar', context.action_lists)  # Aldrachi Reaver
        self.assertIn('fs', context.action_lists)  # Felscarred

        # Verify critical variables
        precombat = context.action_lists['precombat']
        self.assertTrue(any('single_target' in str(action) for action in precombat))
        self.assertTrue(any('small_aoe' in str(action) for action in precombat))
        self.assertTrue(any('big_aoe' in str(action) for action in precombat))

    def test_resource_management(self):
        """Test parsing of soul fragment and fury management"""
        context = self.parser.parse(self.simc_content)
        
        # Verify soul fragment tracking
        default = context.action_lists['default']
        self.assertTrue(any('num_spawnable_souls' in str(action) for action in default))
        
        # Verify fury management
        all_actions = []
        for action_list in context.action_lists.values():
            all_actions.extend(action_list)
        self.assertTrue(any('fury.deficit' in str(action) for action in all_actions))

    def test_defensive_rotation(self):
        """Test parsing of defensive abilities"""
        context = self.parser.parse(self.simc_content)
        
        # Check for defensive abilities
        all_actions = []
        for action_list in context.action_lists.values():
            all_actions.extend(action_list)
            
        defensive_abilities = [
            'demon_spikes',
            'fiery_brand',
            'metamorphosis'
        ]
        
        for ability in defensive_abilities:
            self.assertTrue(
                any(ability in str(action) for action in all_actions),
                f"Missing defensive ability: {ability}"
            )

    def test_spirit_bomb_logic(self):
        """Test parsing of Spirit Bomb decision making"""
        context = self.parser.parse(self.simc_content)
        
        # Check for Spirit Bomb conditions
        all_actions = []
        for action_list in context.action_lists.values():
            all_actions.extend(action_list)
            
        self.assertTrue(any('spirit_bomb' in str(action) for action in all_actions))
        self.assertTrue(any('soul_fragments' in str(action) for action in all_actions))

    def test_aoe_priority(self):
        """Test parsing of AOE priority system"""
        context = self.parser.parse(self.simc_content)
        
        # Check for AOE abilities and conditions
        all_actions = []
        for action_list in context.action_lists.values():
            all_actions.extend(action_list)
            
        aoe_abilities = [
            'immolation_aura',
            'sigil_of_flame',
            'spirit_bomb'
        ]
        
        for ability in aoe_abilities:
            self.assertTrue(
                any(ability in str(action) for action in all_actions),
                f"Missing AOE ability: {ability}"
            )

    def test_lua_generation(self):
        """Test generation of Lua code from parsed VDH APL"""
        context = self.parser.parse(self.simc_content)
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = generator.generate(context.action_lists, {'spec': 'vengeance'})
        
        # Verify critical components
        self.assertIn('function Rotation()', lua_code)
        self.assertIn('function Precombat()', lua_code)
        self.assertIn('function Default()', lua_code)
        
        # Verify defensive rotation
        self.assertIn('Spell.DemonSpikes:IsReady()', lua_code)
        self.assertIn('Spell.FieryBrand:IsReady()', lua_code)
        self.assertIn('Spell.Metamorphosis:IsReady()', lua_code)
        
        # Verify resource management
        self.assertIn('Player.SoulFragments', lua_code)
        self.assertIn('Player.Fury', lua_code)
        
        # Verify AOE abilities
        self.assertIn('Spell.ImmolationAura:IsReady()', lua_code)
        self.assertIn('Spell.SigilOfFlame:IsReady()', lua_code)
        self.assertIn('Spell.SpiritBomb:IsReady()', lua_code)
