"""
Test cooldown management rotation generation
"""
from ...base import PSTestCase
from pathlib import Path

class TestCooldowns(PSTestCase):
    """Test cooldown management rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_cooldowns_generation(self):
        """Test generating cooldown management rotation"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'Cooldowns',
            'profile': 'VDH-Cooldowns',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        self.assertEqual(lua_code.strip(), expected_output.strip())
        self.assertLuaValid(lua_code)
        
    def test_cooldown_conditions(self):
        """Test cooldown condition handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify cooldown conditions
        self.assertIn('Target:TimeToDie() > 30', lua_code)
        self.assertIn('Cache:Get("cooldown_condition")', lua_code)
        self.assertIn('Cache:Get("burst_condition")', lua_code)
        
    def test_trinket_usage(self):
        """Test trinket usage handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify trinket usage
        self.assertIn('Player.Trinket1:IsReady()', lua_code)
        self.assertIn('Player.Trinket2:IsReady()', lua_code) 