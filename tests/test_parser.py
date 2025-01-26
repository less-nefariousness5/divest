"""
Unit tests for SimC parser
"""
from .base import PSTestCase
from ps_simc_parser.parser import Parser

class TestParser(PSTestCase):
    """Test SimC parser functionality"""
    
    def setUp(self):
        """Set up test case"""
        super().setUp()
        self.parser = Parser()
        
    def test_parse_basic_action(self):
        """Test parsing basic action"""
        simc = "actions=immolation_aura"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['type'], 'spell')
        self.assertEqual(result['name'], 'immolation_aura')
        self.assertEqual(result['conditions'], [])
        
    def test_parse_action_with_condition(self):
        """Test parsing action with condition"""
        simc = "actions=fel_devastation,if=fury>50"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['type'], 'spell')
        self.assertEqual(result['name'], 'fel_devastation')
        self.assertEqual(result['conditions'], ['fury>50'])
        
    def test_parse_variable(self):
        """Test parsing variable definition"""
        simc = "variable,name=pool_fury,value=fury>80"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['type'], 'variable')
        self.assertEqual(result['name'], 'pool_fury')
        self.assertEqual(result['value'], 'fury>80')

    def test_parse_action_list(self):
        """Test parsing action list"""
        simc = "actions.defensives=demon_spikes,if=incoming_damage_5s>50000"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['type'], 'spell')
        self.assertEqual(result['name'], 'demon_spikes')
        self.assertEqual(result['list'], 'defensives')
        self.assertEqual(result['conditions'], ['incoming_damage_5s>50000'])

    def test_parse_complex_condition(self):
        """Test parsing complex condition"""
        simc = "actions=spirit_bomb,if=soul_fragments>=4&fury>=30&!buff.metamorphosis.up"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['conditions'], [
            'soul_fragments>=4',
            'fury>=30',
            '!buff.metamorphosis.up'
        ])

    def test_parse_resource_expression(self):
        """Test parsing resource expressions"""
        simc = "actions=soul_cleave,if=fury.deficit<=20"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['conditions'], ['fury.deficit<=20'])

    def test_parse_target_expression(self):
        """Test parsing target expressions"""
        simc = "actions=sigil_of_flame,if=target.time_to_die>8"
        result = self.parser.parse_line(simc)
        
        self.assertEqual(result['conditions'], ['target.time_to_die>8'])

    def test_parse_invalid_syntax(self):
        """Test parsing invalid syntax"""
        with self.assertRaises(Exception):
            self.parser.parse_line("invalid_syntax")

    def test_parse_empty_line(self):
        """Test parsing empty line"""
        result = self.parser.parse_line("")
        self.assertIsNone(result)

    def test_parse_comment(self):
        """Test parsing comment"""
        result = self.parser.parse_line("# This is a comment")
        self.assertIsNone(result)


"""
Tests for the main Parser class that handles the full parsing pipeline.
"""
import unittest
from .base import PSTestCase
from ps_simc_parser.parser import Parser, Action
from ps_simc_parser.parser.exceptions import ParserError

class TestParser(unittest.TestCase):
    """Test the main Parser class"""
    
    def setUp(self):
        """Set up test case"""
        self.parser = Parser()
        self.parser.spec = "vengeance"
        
    def test_parse_file_content(self):
        """Test parsing SimC APL content"""
        simc_content = """
        # Test APL
        actions=auto_attack
        actions+=/infernal_strike,if=!dot.sigil_of_flame.ticking
        actions+=/variable,name=brand_build,value=talent.agonizing_flames.enabled&talent.burning_alive.enabled
        """
        
        # Parse APL content
        actions = self.parser.parse_file_content(simc_content)
        
        # Verify actions were parsed correctly
        self.assertIsNotNone(actions)
        self.assertGreater(len(actions), 0)
        
        # Check first action
        self.assertEqual(actions[0].name, "auto_attack")
        
        # Check second action
        self.assertEqual(actions[1].name, "infernal_strike")
        self.assertEqual(len(actions[1].conditions), 1)
        self.assertEqual(actions[1].conditions[0], "!dot.sigil_of_flame.ticking")
        
        # Check third action
        self.assertEqual(actions[2].name, "variable")
        self.assertEqual(actions[2].args["name"], "brand_build")
        self.assertEqual(actions[2].args["value"], "talent.agonizing_flames.enabled&talent.burning_alive.enabled")
        
if __name__ == '__main__':
    unittest.main()
