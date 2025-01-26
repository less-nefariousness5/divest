"""
Validation tests for PS SimC Parser
"""
from .base import PSTestCase
import json
import lupa

class TestValidation(PSTestCase):
    """Test validation of generated code"""
    
    def setUp(self):
        super().setUp()
        self.lua = lupa.LuaRuntime()
        
    def test_lua_syntax(self):
        """Test Lua syntax validation"""
        actions = self.load_fixture('complex_rotation.json')
        lua_code = self.generator.generate(actions, {})
        
        # Should not raise syntax error
        self.lua.execute(lua_code)
        
    def test_api_compatibility(self):
        """Test PS API compatibility"""
        actions = self.load_fixture('complex_rotation.json')
        lua_code = self.generator.generate(actions, {})
        
        # Check for required API functions
        self.assertIn('Player:AffectingCombat', lua_code)
        self.assertIn('Target:Exists', lua_code)
        self.assertIn('Spell:', lua_code)
        
    def test_resource_validation(self):
        """Test resource validation"""
        actions = [
            {
                'type': 'spell',
                'name': 'fel_devastation',
                'conditions': ['invalid_resource>50']
            }
        ]
        
        with self.assertRaises(Exception):
            self.generator.generate(actions, {})
            
    def test_spell_validation(self):
        """Test spell validation"""
        actions = [
            {
                'type': 'spell',
                'name': 'invalid_spell',
                'conditions': []
            }
        ]
        
        with self.assertRaises(Exception):
            self.generator.generate(actions, {})
            
    def test_condition_validation(self):
        """Test condition validation"""
        actions = [
            {
                'type': 'spell',
                'name': 'fel_devastation',
                'conditions': ['invalid.condition']
            }
        ]
        
        with self.assertRaises(Exception):
            self.generator.generate(actions, {}) 