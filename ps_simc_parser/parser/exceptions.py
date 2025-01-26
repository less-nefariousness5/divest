"""
Exceptions for PS SimC Parser
"""

class ParserError(Exception):
    """Base class for parser errors"""
    def __init__(self, message: str, line_number: int = None, line_content: str = None):
        self.message = message
        self.line_number = line_number
        self.line_content = line_content
        
        error_msg = message
        if line_number is not None:
            error_msg = f"Line {line_number}: {error_msg}"
        if line_content is not None:
            error_msg = f"{error_msg}\n  {line_content}"
            
        super().__init__(error_msg)

class SyntaxError(ParserError):
    """Raised when there is a syntax error in the APL"""
    pass

class CircularReferenceError(ParserError):
    """Raised when there is a circular reference in variable definitions"""
    pass

class DependencyError(ParserError):
    """Raised when there is a missing dependency"""
    pass

class ComplexityError(ParserError):
    """Raised when a condition is too complex"""
    pass

class ValidationError(ParserError):
    """Raised when validation fails"""
    pass
