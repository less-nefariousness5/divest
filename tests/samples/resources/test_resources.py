"""
Test resource management rotation generation
"""
from ...base import PSTestCase
from pathlib import Path

class TestResources(PSTestCase):
    """Test resource management rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_resources_generation(self):
        """Test generating resource management rotation"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'Resources',
            'profile': 'VDH-Resources',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        self.assertEqual(lua_code.strip(), expected_output.strip())
        self.assertLuaValid(lua_code)
        
    def test_resource_variables(self):
        """Test resource variable handling"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        actions = self.parser.parse(simc_input)
        
        variables = [a for a in actions if a['type'] == 'variable']
        self.assertEqual(len(variables), 4)
        self.assertEqual(variables[0]['name'], 'max_fragments')
        self.assertEqual(variables[1]['name'], 'need_fury')
        
    def test_resource_tracking(self):
        """Test resource tracking functions"""
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        lua_code = self.generator.generate(
            self.parser.parse(simc_input),
            {'name': 'test'}
        )
        
        # Verify resource tracking
        self.assertIn('Player:FuryDeficit()', lua_code)
        self.assertIn('Player.SoulFragments', lua_code)
        self.assertIn('Cache:Get("need_fury")', lua_code) 