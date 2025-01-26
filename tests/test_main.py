"""Test main entry point functionality."""

import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from ps_simc_parser.__main__ import cli, parse
from ps_simc_parser.parser import Parser

class TestMain(unittest.TestCase):
    """Test main entry point."""
    
    def setUp(self):
        """Set up test cases."""
        self.runner = CliRunner()
        
    @patch('ps_simc_parser.__main__.Parser')
    def test_parse_interactive(self, mock_parser_class):
        """Test that parse command runs in interactive mode when no args provided."""
        # Create a mock parser instance
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        
        # Call parse command without arguments
        result = self.runner.invoke(cli, ['parse'])
        
        # Assert that parser was initialized and run was called
        mock_parser_class.assert_called_once()
        mock_parser.run.assert_called_once()
        self.assertEqual(result.exit_code, 0)
        
    @patch('ps_simc_parser.__main__.Parser')
    def test_parse_with_args(self, mock_parser_class):
        """Test that parse command handles arguments correctly."""
        # Create a mock parser instance
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        
        # Create a temporary test file
        with self.runner.isolated_filesystem():
            with open('input.simc', 'w') as f:
                f.write('actions=immolation_aura')
                
            # Call parse command with arguments
            result = self.runner.invoke(cli, [
                'parse',
                '--spec', 'vengeance',
                '--input', 'input.simc',
                '--output', 'output.lua'
            ])
            
        # Assert parser methods were called correctly
        mock_parser_class.assert_called_once()
        mock_parser.parse_file.assert_called_once_with('input.simc', 'vengeance')
        mock_parser.generate_lua.assert_called_once()
        self.assertEqual(result.exit_code, 0)
        
    @patch('ps_simc_parser.__main__.Parser')
    def test_parse_missing_args(self, mock_parser_class):
        """Test that parse command falls back to interactive mode with missing args."""
        # Create a mock parser instance
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        
        # Call parse command with partial arguments
        result = self.runner.invoke(cli, ['parse', '--spec', 'vengeance'])
        
        # Assert that parser fell back to interactive mode
        mock_parser_class.assert_called_once()
        mock_parser.run.assert_called_once()
        self.assertEqual(result.exit_code, 0)
        
    def test_cli_help(self):
        """Test that CLI help text is displayed correctly."""
        result = self.runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('PS SimC Parser - Convert SimC APL to PS Lua', result.output)
        
        result = self.runner.invoke(cli, ['parse', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Parse a SimC APL file and convert it to PS Lua', result.output)
