"""
Parser module for PS SimC Parser
"""
from typing import Dict, Any, List, Optional
import click
from ps_simc_parser.parser.apl import APLParser, APLAction, ParserContext
from ps_simc_parser.parser.actions import ActionParser, Action
from ps_simc_parser.utils.constants import SUPPORTED_SPECS

class Parser:
    """Parser class for PS SimC Parser."""
    
    def __init__(self):
        """Initialize parser."""
        self.specs = SUPPORTED_SPECS
        self._spec = None
        self.apl_parser = APLParser()
        self.action_parser = ActionParser()
        
    @property
    def spec(self):
        return self._spec
        
    @spec.setter
    def spec(self, value):
        if value is not None and value not in self.specs:
            raise ValueError(f"Unsupported specialization: {value}")
        self._spec = value
        
    def parse_file_content(self, content: str) -> List[Action]:
        """Parse SimC APL content."""
        if self.spec is None:
            raise ValueError("Specialization must be set before parsing")
            
        context = ParserContext(spec=self.specs[self.spec])
        apl_actions = self.apl_parser.parse(content, context)
        
        # Convert APL actions to PS actions
        return [Action(str(a)) for a in apl_actions]
        
    def parse_file(self, input_file: str) -> List[Action]:
        """Parse a SimC APL file."""
        if self.spec is None:
            raise ValueError("Specialization must be set before parsing")
            
        with open(input_file, 'r') as f:
            content = f.read()
            
        return self.parse_file_content(content)
        
    def generate_lua(self, actions: List[Action]) -> str:
        """Generate Lua code from parsed actions."""
        return self.action_parser.generate_lua(actions)
        
    def run(self):
        """Run the parser."""
        # Parse command line arguments
        input_file = click.prompt("Enter input file path", type=click.Path(exists=True))
        output_file = click.prompt("Enter output file path", type=str)
        
        # Parse APL
        actions = self.parse_file(input_file)
        
        # Generate Lua code
        lua_code = self.generate_lua(actions)
        
        # Write output
        with open(output_file, 'w') as f:
            f.write(lua_code)
            
        return True
