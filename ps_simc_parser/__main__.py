#!/usr/bin/env python3
"""
Main entry point for PS SimC Parser
"""
import click
from pathlib import Path
from .parser import Parser
from .utils.constants import SUPPORTED_SPECS

@click.group()
def cli():
    """PS SimC Parser - Convert SimC APLs to PS Lua"""
    pass

@cli.command()
@click.option('--spec', required=True, type=click.Choice(list(SUPPORTED_SPECS.keys())), help='Specialization to parse')
@click.option('--input', required=True, type=click.Path(exists=True), help='Input SimC file')
@click.option('--output', required=True, type=click.Path(), help='Output Lua file')
def parse(spec, input, output):
    """Parse a SimC file into PS Lua"""
    # Read input file
    with open(input, 'r') as f:
        content = f.read()
        
    # Create parser
    parser = Parser(spec)
    
    # Parse content
    lua_code = parser.parse_file(content)
    
    # Write output file
    with open(output, 'w') as f:
        f.write(lua_code)
        
    click.echo(f"Successfully wrote Lua code to {output}")

if __name__ == '__main__':
    cli()