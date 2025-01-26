"""
Parser module for PS SimC Parser
"""
from typing import Dict, Any, List, Optional
import click
from .parser.apl import APLParser, Action
from .parser.actions import ActionParser
from .utils.constants import SUPPORTED_SPECS

class Parser:
    """Parser class for PS SimC Parser."""
    
    def __init__(self):
        """Initialize parser."""
        self.specs = SUPPORTED_SPECS
        self.apl_parser = APLParser()
        self.action_parser = ActionParser()
        
    def run(self):
        """Run the parser."""
        # Parse command line arguments
        spec = click.prompt("Enter specialization", type=click.Choice(list(self.specs.keys())))
        input_file = click.prompt("Enter input file path", type=click.Path(exists=True))
        output_file = click.prompt("Enter output file path", type=str)
        
        # Read input file
        with open(input_file, 'r') as f:
            content = f.read()
            
        # Parse APL
        actions = self.apl_parser.parse(content, self.specs[spec])
        
        # Generate Lua code
        lua_code = self.action_parser.generate_lua(actions)
        
        # Write output
        with open(output_file, 'w') as f:
            f.write(lua_code)
            
        return True
        
    def parse_file(self, input_file: str, spec: str) -> List[Action]:
        """Parse a SimC APL file."""
        if spec not in self.specs:
            raise ValueError(f"Unsupported specialization: {spec}")
            
        with open(input_file, 'r') as f:
            content = f.read()
            
        return self.apl_parser.parse(content, self.specs[spec])
        
    def generate_lua(self, actions: List[Action]) -> str:
        """Generate Lua code from parsed actions."""
        return self.action_parser.generate_lua(actions)
