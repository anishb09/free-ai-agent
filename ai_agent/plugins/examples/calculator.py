"""
Example calculator plugin
"""

from typing import List, Union
from ..base import BasePlugin, PluginResult
import math
import operator


class CalculatorPlugin(BasePlugin):
    """Simple calculator plugin for basic mathematical operations"""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Performs basic mathematical calculations",
            version="1.0.0"
        )
        
        # Define supported operations
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod,
            '//': operator.floordiv,
        }
        
        # Define supported functions
        self.functions = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            'ceil': math.ceil,
            'floor': math.floor,
        }
    
    async def execute(self, expression: str) -> PluginResult:
        """Execute a mathematical expression"""
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Simple evaluation for basic expressions
            # In a production environment, you'd want more sophisticated parsing
            result = self._safe_eval(expression)
            
            return PluginResult(
                success=True,
                data=result,
                metadata={"expression": expression}
            )
            
        except Exception as e:
            return PluginResult(
                success=False,
                error=f"Calculation error: {str(e)}",
                metadata={"expression": expression}
            )
    
    def _safe_eval(self, expression: str) -> float:
        """Safely evaluate mathematical expressions"""
        # Replace function names with math module equivalents
        for func_name, func in self.functions.items():
            expression = expression.replace(f"{func_name}(", f"math.{func_name}(" if hasattr(math, func_name) else f"{func_name}(")
        
        # Create a safe namespace
        safe_dict = {
            "__builtins__": {},
            "math": math,
            "abs": abs,
            "round": round,
        }
        
        # Add function names to namespace
        safe_dict.update(self.functions)
        
        # Evaluate the expression
        result = eval(expression, safe_dict)
        return result
    
    def get_capabilities(self) -> List[str]:
        """Get calculator capabilities"""
        return [
            "basic_arithmetic",
            "mathematical_functions",
            "trigonometric_functions",
            "logarithmic_functions",
            "expression_evaluation"
        ]
    
    def validate_input(self, expression: str) -> bool:
        """Validate input expression"""
        if not isinstance(expression, str):
            return False
        
        # Check for dangerous keywords
        dangerous_keywords = [
            'import', 'exec', 'eval', 'open', 'file', 'input', 'raw_input',
            '__', 'globals', 'locals', 'vars', 'dir', 'help'
        ]
        
        expression_lower = expression.lower()
        for keyword in dangerous_keywords:
            if keyword in expression_lower:
                return False
        
        return True
    
    async def setup(self) -> None:
        """Setup the calculator plugin"""
        # No special setup needed for calculator
        pass
    
    async def cleanup(self) -> None:
        """Cleanup the calculator plugin"""
        # No cleanup needed for calculator
        pass
