"""
Integration tests for Lua generation
"""
from .base import PSTestCase

class TestLuaGeneration(PSTestCase):
    """Test Lua code generation"""
    
    def test_generate_basic_rotation(self):
        """Test generating basic rotation"""
        actions = [
            {
                'type': 'spell',
                'name': 'immolation_aura',
                'conditions': []
            },
            {
                'type': 'spell',
                'name': 'fel_devastation',
                'conditions': ['fury>50']
            }
        ]
        
        context = {
            'name': 'Test Rotation',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank'
        }
        
        lua_code = self.generator.generate(actions, context)
        self.assertLuaValid(lua_code)
        self.assertMetricsValid()
        
    def test_generate_with_mechanics(self):
        """Test generating rotation with mechanics"""
        context = {
            'use_mechanics': True,
            'name': 'Test Rotation',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank'
        }
        
        actions = [
            {
                'type': 'spell',
                'name': 'infernal_strike',
                'conditions': ['not.in.position']
            }
        ]
        
        lua_code = self.generator.generate(actions, context)
        self.assertLuaValid(lua_code)
        self.assertIn('HandleMechanics', lua_code)
        self.assertIn('HandleMovement', lua_code)

    def test_generate_with_variables(self):
        """Test generating rotation with variables"""
        actions = [
            {
                'type': 'variable',
                'name': 'use_defensives',
                'value': 'health.pct<65'
            },
            {
                'type': 'spell',
                'name': 'demon_spikes',
                'conditions': ['variable.use_defensives']
            }
        ]
        
        lua_code = self.generator.generate(actions, {})
        self.assertLuaValid(lua_code)
        self.assertIn('Cache:Set("use_defensives"', lua_code)

    def test_generate_with_action_lists(self):
        """Test generating rotation with action lists"""
        actions = [
            {
                'type': 'call_action_list',
                'name': 'defensives',
                'conditions': ['health.pct<65']
            }
        ]
        
        action_lists = {
            'defensives': [
                {
                    'type': 'spell',
                    'name': 'demon_spikes',
                    'conditions': []
                }
            ]
        }
        
        context = {'action_lists': action_lists}
        lua_code = self.generator.generate(actions, context)
        
        self.assertLuaValid(lua_code)
        self.assertIn('function Rotation:defensives', lua_code)

    def test_generate_with_resources(self):
        """Test generating rotation with resource handling"""
        actions = [
            {
                'type': 'spell',
                'name': 'soul_cleave',
                'conditions': ['fury>=60', 'soul_fragments>=2']
            }
        ]
        
        lua_code = self.generator.generate(actions, {})
        self.assertLuaValid(lua_code)
        self.assertIn('Player.Fury', lua_code)
        self.assertIn('Player.SoulFragments', lua_code)

    def test_generate_with_buffs(self):
        """Test generating rotation with buff handling"""
        actions = [
            {
                'type': 'spell',
                'name': 'fel_devastation',
                'conditions': ['!buff.metamorphosis.up']
            }
        ]
        
        lua_code = self.generator.generate(actions, {})
        self.assertLuaValid(lua_code)
        self.assertIn('Player.Buff', lua_code)

    def test_generate_with_targeting(self):
        """Test generating rotation with targeting"""
        actions = [
            {
                'type': 'spell',
                'name': 'throw_glaive',
                'conditions': ['target.distance>8']
            }
        ]
        
        lua_code = self.generator.generate(actions, {})
        self.assertLuaValid(lua_code)
        self.assertIn('Target.Distance', lua_code)

    def test_error_handling(self):
        """Test error handling in generation"""
        with self.assertRaises(Exception):
            self.generator.generate(None, {}) 