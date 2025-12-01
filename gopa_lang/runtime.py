"""Runtime environment for Gopa interpreter."""

from typing import Dict, Any, Optional
from copy import deepcopy


class Runtime:
    """Runtime environment with dynamic scoping and closures."""
    
    def __init__(self, parent: Optional['Runtime'] = None):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Any] = {}
        self.parent = parent
    
    def get(self, name: str) -> Any:
        """Get variable from current or parent scope."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Variable '{name}' not defined")
    
    def set(self, name: str, value: Any):
        """Set variable in current scope."""
        self.variables[name] = value
    
    def define_function(self, name: str, func):
        """Define a function in current scope."""
        self.functions[name] = func
    
    def get_function(self, name: str):
        """Get function from current or parent scope."""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise NameError(f"Function '{name}' not defined")
    
    def child_scope(self) -> 'Runtime':
        """Create a child scope with closure."""
        child = Runtime(self)
        child.functions = deepcopy(self.functions)
        return child
    
    def has(self, name: str) -> bool:
        """Check if variable exists in current or parent scope."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False

