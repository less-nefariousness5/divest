"""Test APL parser functionality."""

import unittest
from ps_simc_parser.parser.apl import APLParser, Action

class TestAPLParser(unittest.TestCase):
    """Test APL parser functionality."""
    
    def setUp(self):
        """Set up test cases."""
        self.parser = APLParser()
        
    def test_parse_simple_action(self):
        """Test parsing a simple action without conditions."""
        content = "actions=immolation_aura"
        actions = self.parser.parse(content, None)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "immolation_aura")
        self.assertEqual(actions[0].conditions, [])
        self.assertEqual(actions[0].args, {})
        
    def test_parse_action_with_condition(self):
        """Test parsing an action with conditions."""
        content = "actions=spirit_bomb,if=soul_fragments>=4"
        actions = self.parser.parse(content, None)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "spirit_bomb")
        self.assertEqual(actions[0].conditions, ["soul_fragments>=4"])
        self.assertEqual(actions[0].args, {})
        
    def test_parse_action_with_args(self):
        """Test parsing an action with arguments."""
        content = "actions=sigil_of_flame,target=ground,if=!debuff.sigil_of_flame.up"
        actions = self.parser.parse(content, None)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "sigil_of_flame")
        self.assertEqual(actions[0].conditions, ["!debuff.sigil_of_flame.up"])
        self.assertEqual(actions[0].args, {"target": "ground"})
        
    def test_parse_multiple_actions(self):
        """Test parsing multiple actions."""
        content = """
        actions=immolation_aura
        actions+=/spirit_bomb,if=soul_fragments>=4
        actions+=/sigil_of_flame,target=ground,if=!debuff.sigil_of_flame.up
        """
        actions = self.parser.parse(content, None)
        
        self.assertEqual(len(actions), 3)
        # First action
        self.assertEqual(actions[0].name, "immolation_aura")
        self.assertEqual(actions[0].conditions, [])
        # Second action
        self.assertEqual(actions[1].name, "spirit_bomb")
        self.assertEqual(actions[1].conditions, ["soul_fragments>=4"])
        # Third action
        self.assertEqual(actions[2].name, "sigil_of_flame")
        self.assertEqual(actions[2].conditions, ["!debuff.sigil_of_flame.up"])
        self.assertEqual(actions[2].args, {"target": "ground"})
        
    def test_parse_variable(self):
        """Test parsing variable definitions."""
        content = "variable,name=brand_build,value=talent.burning_brand.enabled"
        actions = self.parser.parse(content, None)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "variable")
        self.assertEqual(actions[0].args, {
            "name": "brand_build",
            "value": "talent.burning_brand.enabled"
        })
        
    def test_parse_complex_conditions(self):
        """Test parsing complex conditions with multiple operators."""
        content = "actions=fel_devastation,if=!buff.metamorphosis.up&fury>=50&incoming_damage_5s>0"
        actions = self.parser.parse(content, None)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "fel_devastation")
        self.assertEqual(actions[0].conditions, [
            "!buff.metamorphosis.up",
            "fury>=50",
            "incoming_damage_5s>0"
        ])
        
    def test_invalid_syntax(self):
        """Test handling of invalid syntax."""
        with self.assertRaises(ValueError):
            self.parser.parse("invalid_syntax=something", None)
            
    def test_empty_input(self):
        """Test handling of empty input."""
        actions = self.parser.parse("", None)
        self.assertEqual(len(actions), 0)
        
        actions = self.parser.parse("\n\n", None)
        self.assertEqual(len(actions), 0)
        
    def test_comment_handling(self):
        """Test handling of comments in APL."""
        content = """
        # This is a comment
        actions=immolation_aura
        actions+=/spirit_bomb,if=soul_fragments>=4 # Inline comment
        // Another comment style
        actions+=/sigil_of_flame
        """
        actions = self.parser.parse(content, None)
        self.assertEqual(len(actions), 3)
        self.assertEqual(actions[0].name, "immolation_aura")
        self.assertEqual(actions[1].name, "spirit_bomb")
        self.assertEqual(actions[2].name, "sigil_of_flame")
        
    def test_malformed_conditions(self):
        """Test handling of malformed conditions."""
        invalid_conditions = [
            "actions=spell,if=",  # Empty condition
            "actions=spell,if=&&",  # Invalid operators
            "actions=spell,if=||",
            "actions=spell,if=condition&&",  # Incomplete condition
            "actions=spell,if=&condition"  # Invalid operator position
        ]
        
        for condition in invalid_conditions:
            with self.assertRaises(ValueError, msg=f"Should fail on: {condition}"):
                self.parser.parse(condition, None)
                
    def test_malformed_arguments(self):
        """Test handling of malformed arguments."""
        invalid_args = [
            "actions=spell,=value",  # Missing argument name
            "actions=spell,arg=",  # Missing argument value
            "actions=spell,arg==value",  # Invalid operator
            "actions=spell,arg=value=extra"  # Multiple equal signs
        ]
        
        for arg in invalid_args:
            with self.assertRaises(ValueError, msg=f"Should fail on: {arg}"):
                self.parser.parse(arg, None)
                
    def test_line_continuation(self):
        """Test handling of line continuation."""
        content = """
        actions=immolation_aura,\\
               if=!buff.metamorphosis.up&\\
               fury>=50
        """
        actions = self.parser.parse(content, None)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "immolation_aura")
        self.assertEqual(len(actions[0].conditions), 2)
        self.assertEqual(actions[0].conditions, ["!buff.metamorphosis.up", "fury>=50"])
