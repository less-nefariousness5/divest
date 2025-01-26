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
