"""
Test complex rotation generation
"""
from ...base import PSTestCase
from pathlib import Path

class TestComplex(PSTestCase):
    """Test complex rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_complex_generation(self):
        """Test generating complex rotation"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'Complex',
            'profile': 'VDH-Complex',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        self.assertEqual(lua_code.strip(), expected_output.strip())
        self.assertLuaValid(lua_code)
        
    def test_complex_variable_handling(self):
        """Test complex variable handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        actions = self.parser.parse(simc_input)
        
        variables = [a for a in actions if a['type'] == 'variable']
        self.assertEqual(len(variables), 3)
        self.assertEqual(variables[0]['name'], 'defensive_condition')
        self.assertEqual(variables[1]['name'], 'emergency_condition')
        self.assertEqual(variables[2]['name'], 'pool_fury')
        
    def test_complex_conditions(self):
        """Test complex condition handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify complex conditions
        self.assertIn('Player:HealthPercent() < 65', lua_code)
        self.assertIn('Player:IncomingDamage(5) > 100000', lua_code)
        self.assertIn('Player.Buff(Spell.Metamorphosis):Exists()', lua_code)
        self.assertIn('Cache:Get("emergency_condition")', lua_code) 