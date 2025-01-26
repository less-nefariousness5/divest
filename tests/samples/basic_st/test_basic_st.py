"""
Test basic single target rotation
"""
from ...base import PSTestCase
from pathlib import Path

class TestBasicST(PSTestCase):
    """Test basic single target rotation generation"""
    
    def setUp(self):
        super().setUp()
        self.sample_dir = Path(__file__).parent
        
    def test_basic_st_generation(self):
        """Test generating basic single target rotation"""
        # Load SimC input
        simc_input = (self.sample_dir / 'rotation.simc').read_text()
        
        # Load expected output
        expected_output = (self.sample_dir / 'expected.lua').read_text()
        
        # Parse and generate
        actions = self.parser.parse(simc_input)
        lua_code = self.generator.generate(actions, {
            'name': 'Basic ST',
            'profile': 'VDH-Basic',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
        })
        
        # Compare with expected
        self.assertEqual(lua_code.strip(), expected_output.strip())
        
        # Validate Lua syntax
        self.assertLuaValid(lua_code) 