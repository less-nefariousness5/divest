"""
Test AOE rotation generation
"""
from ...base import PSTestCase
from pathlib import Path

class TestAOE(PSTestCase):
    """Test AOE rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_aoe_generation(self):
        """Test generating AOE rotation"""
        # Load SimC input
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        
        # Load expected output
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        # Parse and generate
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'AOE',
            'profile': 'VDH-AOE',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        # Set maxDiff to None to see full diff
        self.maxDiff = None
        
        # Compare with expected
        self.assertEqual(lua_code.strip(), expected_output.strip())
        
        # Validate Lua syntax
        self.assertLuaValid(lua_code)
        
    def test_aoe_variable_handling(self):
        """Test AOE variable handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        actions = self.parser.parse(simc_input)
        
        # Verify variables are parsed correctly
        variables = [a for a in actions if a['type'] == 'variable']
        self.assertEqual(len(variables), 2)
        self.assertEqual(variables[0]['name'], 'large_pull')
        self.assertEqual(variables[1]['name'], 'use_defensives')
        
    def test_aoe_enemy_counting(self):
        """Test AOE enemy counting logic"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify enemy count checks
        self.assertIn('Enemies:Count() >= 3', lua_code)
        self.assertIn('Enemies:Count() > 1', lua_code)
        self.assertIn('Enemies:Count() >= 2', lua_code) 