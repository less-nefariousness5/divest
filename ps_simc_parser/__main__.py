#!/usr/bin/env python3
"""Main entry point for PS SimC Parser"""

import click
from ps_simc_parser.parser import Parser
from ps_simc_parser.utils.constants import SUPPORTED_SPECS

@click.group()
def cli():
    """PS SimC Parser - Convert SimC APL to PS Lua"""
    pass

@cli.command()
@click.option('--spec', type=click.Choice(list(SUPPORTED_SPECS.keys())), help='Specialization to parse')
@click.option('--input', type=click.Path(exists=True), help='Input SimC file')
@click.option('--output', type=str, help='Output Lua file')
def parse(spec=None, input=None, output=None):
    """Parse a SimC APL file and convert it to PS Lua"""
    parser = Parser()
    
    if spec and input and output:
        # Parse file directly if all arguments provided
        actions = parser.parse_file(input, spec)
        lua_code = parser.generate_lua(actions)
        with open(output, 'w') as f:
            f.write(lua_code)
    else:
        # Run interactive mode
        parser.run()
        
    return True

if __name__ == "__main__":
    cli()