"""
Edge case tests for PS SimC Parser.
Tests various error conditions and edge cases to ensure robust error handling.
"""
import unittest
from .base import PSTestCase
from ps_simc_parser.parser.exceptions import (
    ParserError, SyntaxError, CircularReferenceError,
    DependencyError, ComplexityError, ValidationError
)
from ps_simc_parser.parser.apl import APLParser

class TestEdgeCases(PSTestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        super().setUp()
        self.apl_parser = APLParser()
        # Set up known spells/buffs for testing
        self.apl_parser.known_spells = {
            'auto_attack', 'spell_name', 'valid_spell', 'another_spell',
            'spell', 'variable', 'name', 'buff', 'cooldown', 'target',
            'resource', 'missing_spell', 'nonexistent'
        }
        self.invalid_simc = {
            'syntax_error': """
                # Invalid syntax in APL
                actions=auto_attack
                actions+=/spell_name,if==buff.name.up  # Double equals
                actions+=/another_spell,if=resource>   # Missing value after operator
            """,
            'circular_reference': """
                # Circular variable references
                actions=auto_attack
                actions+=/variable,name=var1,value=variable.var2
                actions+=/variable,name=var2,value=variable.var1
            """,
            'missing_dependency': """
                # Missing spell dependencies
                actions=auto_attack
                actions+=/unknown_spell,if=buff.name.up
                actions+=/another_spell,if=buff.unknown.up
            """,
            'invalid_operators': """
                # Invalid operators in conditions
                actions=auto_attack
                actions+=/spell_name,if=buff.name.up !! target.health>50  # Invalid operator !!
                actions+=/spell_name,if=buff.name.up >< target.health>50  # Invalid operator ><
            """,
            'malformed_actions': """
                # Malformed action lines
                actions=auto_attack
                actions+=/,if=buff.name.up  # Missing spell name
                actions+=/spell_name,  # Missing condition
                actions+=spell_name  # Missing forward slash
            """,
            'nested_parentheses': """
                # Deeply nested parentheses
                actions=auto_attack
                actions+=/spell_name,if=buff.name.up&(cooldown.spell.remains<5)&(target.health.pct<20)
            """,
            'special_characters': """
                # Special characters in names
                actions=auto_attack
                actions+=/spell@name,if=buff.name.up
                actions+=/spell$name,if=buff.name.up
            """,
            'whitespace_handling': """
                # Various whitespace cases
                actions=auto_attack
                actions+=/spell_name,if=buff.name.up&target.health.pct<50
                actions+=/spell_name,if=buff.name.up & target.health.pct < 50
                actions+=/spell_name,if=buff.name.up&target.health.pct<50
            """
        }

    def test_syntax_error_handling(self):
        """Test handling of syntax errors in APL"""
        with self.assertRaises(SyntaxError) as context:
            self.apl_parser.parse(self.invalid_simc['syntax_error'])
        
        self.assertIn('double equals', str(context.exception).lower())

    def test_circular_reference_detection(self):
        """Test detection of circular variable references"""
        with self.assertRaises(CircularReferenceError) as context:
            self.apl_parser.parse(self.invalid_simc['circular_reference'])
        
        self.assertIn('circular reference', str(context.exception).lower())

    def test_missing_dependency_handling(self):
        """Test handling of missing spell/buff dependencies"""
        with self.assertRaises(DependencyError) as context:
            self.apl_parser.parse(self.invalid_simc['missing_dependency'])
        
        self.assertIn('unknown spell', str(context.exception).lower())

    def test_invalid_operator_handling(self):
        """Test handling of invalid operators in conditions"""
        with self.assertRaises(SyntaxError) as context:
            self.apl_parser.parse(self.invalid_simc['invalid_operators'])
        
        self.assertIn('invalid operator', str(context.exception).lower())

    def test_malformed_action_handling(self):
        """Test handling of malformed action lines"""
        with self.assertRaises(SyntaxError) as context:
            self.apl_parser.parse(self.invalid_simc['malformed_actions'])
        
        self.assertIn('missing action name', str(context.exception).lower())

    def test_nested_parentheses_handling(self):
        """Test handling of deeply nested parentheses"""
        try:
            actions = self.apl_parser.parse(self.invalid_simc['nested_parentheses'])
            # Should parse successfully
            self.assertTrue(any('spell_name' in str(action) for action in actions))
        except ComplexityError as e:
            # Also acceptable if parser rejects overly complex conditions
            self.assertIn('complex', str(e).lower())

    def test_special_character_handling(self):
        """Test handling of special characters in names"""
        with self.assertRaises(ValidationError) as context:
            self.apl_parser.parse(self.invalid_simc['special_characters'])
        
        self.assertIn('invalid characters', str(context.exception).lower())

    def test_whitespace_handling(self):
        """Test handling of various whitespace cases"""
        try:
            actions = self.apl_parser.parse(self.invalid_simc['whitespace_handling'])
            
            # All three actions should parse to equivalent conditions
            conditions = [str(action) for action in actions if action.spell_name == 'spell_name']
            self.assertTrue(all(cond == conditions[0] for cond in conditions),
                          "Different whitespace resulted in different conditions")
        except ParserError as e:
            self.fail(f"Parser failed to handle whitespace variations: {e}")

    def test_error_recovery(self):
        """Test parser's ability to recover from errors"""
        # Mix of valid and invalid actions
        mixed_simc = """
            actions=auto_attack
            actions+=/valid_spell
            actions+=/invalid@spell,if=buff.name.up  # Should fail
            actions+=/another_spell,if=buff.name.up
        """
        
        with self.assertRaises(ValidationError) as context:
            self.apl_parser.parse(mixed_simc)
        
        # Error message should indicate line number
        error_msg = str(context.exception).lower()
        self.assertIn('line', error_msg)
        self.assertIn('invalid@spell', error_msg)

    def test_empty_input_handling(self):
        """Test handling of empty or whitespace-only input"""
        empty_cases = ['', ' ', '\n', '\t', '  \n  \t  ']
        
        for case in empty_cases:
            with self.assertRaises(ValidationError) as context:
                self.apl_parser.parse(case)
            self.assertIn('empty', str(context.exception).lower())

    def test_max_complexity_handling(self):
        """Test handling of overly complex conditions"""
        # Generate a deeply nested condition with many operators
        deep_nesting = """
            actions=auto_attack
            actions+=/spell,if=buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up&buff.name.up
        """
        
        with self.assertRaises(ComplexityError) as context:
            self.apl_parser.parse(deep_nesting)
        
        self.assertIn('complex', str(context.exception).lower())

if __name__ == '__main__':
    unittest.main()
