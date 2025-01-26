"""
Base test class for PS SimC Parser tests
"""
import unittest
import json
from pathlib import Path
from ps_simc_parser.parser import Parser
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.parser.apl import ParserContext
import lupa
from typing import Any, Dict
import os

class PSTestCase(unittest.TestCase):
    """Base test class with common test functionality"""
    
    def setUp(self):
        """Set up test case with parser, generator, and default context"""
        self.parser = Parser()
        self.generator = LuaGenerator()
        self.lua = lupa.LuaRuntime()
        self.test_dir = Path(__file__).parent
        self.fixtures_dir = self.test_dir / 'fixtures'
        self.output_dir = self.test_dir / 'output'
        self.output_dir.mkdir(exist_ok=True)
        
        self.default_context = {
            'name': 'Test Rotation',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
            'level': 70,
            'spells': {
                'auto_attack',
                'infernal_strike',
                'sigil_of_flame',
                'immolation_aura',
                'fel_devastation',
                'spirit_bomb',
                'soul_cleave',
                'fracture',
                'shear',
                'throw_glaive',
                'demon_spikes',
                'metamorphosis',
                'fiery_brand',
                'bulk_extraction',
                'felblade',
            },
            'buffs': {
                'metamorphosis',
                'demon_spikes',
                'fiery_brand',
                'soul_fragments',
                'sigil_of_flame',
            },
            'talents': {
                'agonizing_flames',
                'burning_alive',
                'charred_flesh',
                'fallout',
                'feed_the_demon',
                'fracture',
                'spirit_bomb',
            }
        }
        
    def tearDown(self):
        """Clean up after test"""
        # Clean output directory
        for file in self.output_dir.glob('*'):
            file.unlink()
            
    def load_fixture(self, name: str) -> Dict:
        """Load test fixture file"""
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', f'{name}')
        with open(fixture_path, 'r') as f:
            content = f.read()
            
            # If it's a SimC file, parse it with the parser
            if name.endswith('.simc'):
                return self.parser.parse_file_content(content)
            else:
                return json.loads(content)
                
    def save_output(self, name: str, content: str):
        """Save test output to file"""
        output_path = os.path.join(os.path.dirname(__file__), 'output', f'{name}')
        with open(output_path, 'w') as f:
            f.write(content)
            
    def assertLuaValid(self, lua_code: str):
        """Assert that Lua code is valid"""
        try:
            self.lua.execute(lua_code)
        except Exception as e:
            self.fail(f"Invalid Lua code: {str(e)}\n{lua_code}")
            
    def assertLuaEqual(self, expected: Any, actual: Any):
        """Assert that two Lua values are equal"""
        self.assertEqual(str(expected), str(actual))