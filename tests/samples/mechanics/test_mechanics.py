"""
Test mechanic handling rotation generation
"""
from ...base import PSTestCase
from pathlib import Path

class TestMechanics(PSTestCase):
    """Test mechanic handling rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_mechanics_generation(self):
        """Test generating mechanics rotation"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'Mechanics',
            'profile': 'VDH-Mechanics',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        self.assertEqual(lua_code.strip(), expected_output.strip())
        self.assertLuaValid(lua_code)
        
    def test_mechanic_detection(self):
        """Test mechanic detection functions"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify mechanic detection
        self.assertIn('Mechanics:MovementRequired()', lua_code)
        self.assertIn('Mechanics:DodgeRequired()', lua_code)
        self.assertIn('Mechanics:ImmunityRequired()', lua_code)
        self.assertIn('Mechanics:FrontalActive()', lua_code)
        
    def test_mechanic_responses(self):
        """Test mechanic response actions"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        actions = self.parser.parse(simc_input)
        
        # Verify mechanic responses
        mechanic_actions = [a for a in actions if 'mechanic' in str(a.get('conditions', []))]
        self.assertGreater(len(mechanic_actions), 0)
        
        # Verify safety checks
        lua_code = self.generator.generate(actions, {'name': 'test'})
        self.assertIn('Cache:Get("safe_to_attack")', lua_code) 