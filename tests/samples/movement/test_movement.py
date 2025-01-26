"""
Test movement and positioning rotation generation
"""
from ...base import PSTestCase
from pathlib import Path

class TestMovement(PSTestCase):
    """Test movement and positioning rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_movement_generation(self):
        """Test generating movement rotation"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'Movement',
            'profile': 'VDH-Movement',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        self.assertEqual(lua_code.strip(), expected_output.strip())
        self.assertLuaValid(lua_code)
        
    def test_position_checks(self):
        """Test position checking functions"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify position checks
        self.assertIn('Target:Distance()', lua_code)
        self.assertIn('Position:InAvoidZone()', lua_code)
        self.assertIn('Position:HasSafeLocation()', lua_code)
        self.assertIn('Position:InVoidZone()', lua_code)
        
    def test_movement_abilities(self):
        """Test movement ability handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify movement abilities
        self.assertIn('Spell.InfernalStrike:IsReady()', lua_code)
        self.assertIn('Spell.Felblade:IsReady()', lua_code)
        self.assertIn('Spell.ThrowGlaive:IsReady()', lua_code) 