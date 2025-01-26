"""
Integration tests for Lua generation
"""
from .base import PSTestCase
from ps_simc_parser.lua_gen.generator import LuaGenerator

class TestLuaGeneration(PSTestCase):
    """Test Lua code generation"""
    
    def setUp(self):
        super().setUp()
        self.generator = LuaGenerator()
    
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
        self.assertMetricsValid()

class ComprehensiveLuaGenerationTest(PSTestCase):
    """Comprehensive tests for Lua code generation"""
    
    def setUp(self):
        super().setUp()
        self.generator = LuaGenerator()
    
    def test_basic_spell_generation(self):
        """Test generation of basic spell casting"""
        actions = [
            {
                'type': 'spell',
                'name': 'immolation_aura',
                'conditions': []
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Spell.ImmolationAura:Cast()', lua_code)
    
    def test_conditional_spell_generation(self):
        """Test generation of conditional spell casting"""
        actions = [
            {
                'type': 'spell',
                'name': 'fel_devastation',
                'conditions': ['fury>=50']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('if Player.Fury >= 50 then', lua_code)
    
    def test_variable_generation(self):
        """Test generation of variable operations"""
        actions = [
            {
                'type': 'variable',
                'name': 'pool_for_meta',
                'value': 'fury>=80'
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Cache:Set("pool_for_meta"', lua_code)
    
    def test_action_list_generation(self):
        """Test generation of action lists"""
        actions = [
            {
                'type': 'call_action_list',
                'name': 'defensives',
                'conditions': ['incoming_damage_5s>100000']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('if Defensives() then', lua_code)
    
    def test_resource_conditions(self):
        """Test generation of resource conditions"""
        actions = [
            {
                'type': 'spell',
                'name': 'soul_cleave',
                'conditions': ['fury>=60', 'soul_fragments>=3']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Player.Fury >= 60', lua_code)
        self.assertIn('Player.SoulFragments >= 3', lua_code)
    
    def test_target_conditions(self):
        """Test generation of target conditions"""
        actions = [
            {
                'type': 'spell',
                'name': 'fiery_brand',
                'conditions': ['target.time_to_die>8']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Target.TimeToDie > 8', lua_code)
    
    def test_complex_expressions(self):
        """Test generation of complex expressions"""
        actions = [
            {
                'type': 'spell',
                'name': 'metamorphosis',
                'conditions': [
                    'soul_fragments>=4',
                    'fury>=30',
                    '!buff.metamorphosis.up'
                ]
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Player.SoulFragments >= 4', lua_code)
        self.assertIn('Player.Fury >= 30', lua_code)
        self.assertIn('not Player:HasBuff(Spell.Metamorphosis)', lua_code)
    
    def test_precombat_generation(self):
        """Test generation of precombat actions"""
        actions = [
            {
                'type': 'spell',
                'name': 'sigil_of_flame',
                'target': 'ground'
            }
        ]
        lua_code = self.generator.generate(actions, {'precombat': True})
        self.assertLuaValid(lua_code)
        self.assertIn('function Precombat()', lua_code)
    
    def test_defensive_generation(self):
        """Test generation of defensive abilities"""
        actions = [
            {
                'type': 'spell',
                'name': 'demon_spikes',
                'conditions': ['incoming_damage_3s>50000']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Player:IncomingDamage(3) > 50000', lua_code)
    
    def test_aoe_generation(self):
        """Test generation of AOE conditions"""
        actions = [
            {
                'type': 'spell',
                'name': 'spirit_bomb',
                'conditions': ['active_enemies>=3']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Player:GetEnemiesInRange(8) >= 3', lua_code)
    
    def test_talent_conditions(self):
        """Test generation of talent conditions"""
        actions = [
            {
                'type': 'spell',
                'name': 'fracture',
                'conditions': ['talent.fracture.enabled']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Player:HasTalent(Spell.Fracture)', lua_code)
    
    def test_full_rotation_generation(self):
        """Test generation of a complete rotation"""
        actions = [
            {
                'type': 'variable',
                'name': 'brand_target',
                'value': 'target.time_to_die>8'
            },
            {
                'type': 'spell',
                'name': 'fiery_brand',
                'conditions': ['variable.brand_target']
            },
            {
                'type': 'call_action_list',
                'name': 'defensives',
                'conditions': ['incoming_damage_5s>100000']
            },
            {
                'type': 'spell',
                'name': 'spirit_bomb',
                'conditions': ['soul_fragments>=4', 'active_enemies>=3']
            }
        ]
        lua_code = self.generator.generate(actions, self.default_context)
        self.assertLuaValid(lua_code)
        self.assertIn('Cache:Set("brand_target"', lua_code)
        self.assertIn('if Defensives() then', lua_code)
        self.assertIn('Player:GetEnemiesInRange(8) >= 3', lua_code)