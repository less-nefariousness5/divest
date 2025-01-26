"""Test database functionality."""

import unittest
from ps_simc_parser.database import (
    get_spell_info,
    get_resource_info,
    get_expression_mapping,
    get_tier_bonus,
    get_racial_ability,
    get_trinket_effect,
    get_combat_mechanic,
    SPELL_INFO,
    RESOURCE_INFO,
    EXPRESSION_MAPPINGS,
    TIER_SET_INFO,
    RACIAL_INFO,
    TRINKET_INFO,
    COMBAT_MECHANICS
)

class TestDatabase(unittest.TestCase):
    """Test database functionality."""
    
    def test_get_spell_info(self):
        """Test getting spell information."""
        # Test valid spell
        spell_info = get_spell_info('vengeance', 'immolation_aura')
        self.assertTrue(spell_info)  # Not empty dict
        self.assertEqual(spell_info['id'], 258920)
        self.assertEqual(spell_info['name'], 'Immolation Aura')
        self.assertEqual(spell_info['type'], 'spell')
        self.assertEqual(spell_info['range'], 8)
        self.assertTrue(spell_info['gcd'])
        
        # Test spell with resource cost
        spell_info = get_spell_info('vengeance', 'fel_devastation')
        self.assertTrue(spell_info)  # Not empty dict
        self.assertEqual(spell_info['resource_cost'], 50)
        self.assertEqual(spell_info['resource_type'], 'fury')
        
        # Test spell with requirements
        spell_info = get_spell_info('vengeance', 'spirit_bomb')
        self.assertTrue(spell_info)  # Not empty dict
        self.assertEqual(spell_info['requires'], 'soul_fragments')
        
        # Test invalid spell
        spell_info = get_spell_info('vengeance', 'nonexistent_spell')
        self.assertEqual(spell_info, {})
            
    def test_get_resource_info(self):
        """Test getting resource information."""
        # Test fury resource
        resource_info = get_resource_info('fury')
        self.assertTrue(resource_info)  # Not empty dict
        self.assertEqual(resource_info['type'], 'primary')
        self.assertEqual(resource_info['max'], 120)
        self.assertEqual(resource_info['min'], 0)
        
        # Test soul fragments resource
        resource_info = get_resource_info('soul_fragments')
        self.assertTrue(resource_info)  # Not empty dict
        self.assertEqual(resource_info['type'], 'secondary')
        self.assertEqual(resource_info['max'], 5)
        
        # Test invalid resource
        resource_info = get_resource_info('nonexistent_resource')
        self.assertEqual(resource_info, {})
            
    def test_get_expression_mapping(self):
        """Test getting expression mappings."""
        # Test resource expressions
        self.assertEqual(get_expression_mapping('fury'), 'Player.Fury')
        self.assertEqual(get_expression_mapping('soul_fragments'), 'Player.SoulFragments')
        
        # Test invalid expression
        expr_mapping = get_expression_mapping('nonexistent_expression')
        self.assertEqual(expr_mapping, '')
            
    def test_get_tier_bonus(self):
        """Test getting tier set bonus information."""
        # Test T29 2pc
        bonus_info = get_tier_bonus('vengeance', '29', 2)
        self.assertTrue(bonus_info)  # Not empty dict
        self.assertEqual(bonus_info['name'], 'Blazing Determination')
        self.assertEqual(bonus_info['type'], 'buff')
        
        # Test invalid tier
        bonus_info = get_tier_bonus('vengeance', '999', 2)
        self.assertEqual(bonus_info, {})
            
    def test_get_racial_ability(self):
        """Test getting racial ability information."""
        # Test valid racial
        racial_info = get_racial_ability('bloodelf', 'arcane_torrent')
        self.assertTrue(racial_info)  # Not empty dict
        self.assertEqual(racial_info['name'], 'Arcane Torrent')
        self.assertEqual(racial_info['type'], 'spell')
        self.assertEqual(racial_info['resource_gain'], 15)
        self.assertEqual(racial_info['resource_type'], 'fury')
        
        # Test invalid racial
        racial_info = get_racial_ability('invalid_race', 'invalid_ability')
        self.assertEqual(racial_info, {})
            
    def test_get_trinket_effect(self):
        """Test getting trinket effect information."""
        # Test valid trinket
        trinket_info = get_trinket_effect('algethar_puzzle_box')
        self.assertTrue(trinket_info)  # Not empty dict
        self.assertEqual(trinket_info['name'], "Algeth'ar Puzzle Box")
        self.assertEqual(trinket_info['type'], 'spell')
        self.assertEqual(trinket_info['cooldown'], 180)
        
        # Test invalid trinket
        trinket_info = get_trinket_effect('nonexistent_trinket')
        self.assertEqual(trinket_info, {})
            
    def test_get_combat_mechanic(self):
        """Test getting combat mechanic information."""
        # Test valid mechanic
        mechanic_info = get_combat_mechanic('player', 'active_mitigation')
        self.assertTrue(mechanic_info)  # Not empty string
        self.assertEqual(mechanic_info, 'Player:HasActiveMitigation()')
        
        # Test invalid mechanic
        mechanic_info = get_combat_mechanic('invalid_type', 'invalid_mechanic')
        self.assertEqual(mechanic_info, '')
