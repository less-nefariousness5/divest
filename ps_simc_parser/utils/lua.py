"""Lua code generation utilities."""

class LuaGenerator:
    """Utility class for generating Lua code."""
    
    def __init__(self):
        """Initialize the generator."""
        self.indent_level = 0
        self.indent_str = "    "
        
    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1
        
    def dedent(self):
        """Decrease indentation level."""
        if self.indent_level > 0:
            self.indent_level -= 1
            
    def get_indent(self):
        """Get current indentation string."""
        return self.indent_str * self.indent_level
