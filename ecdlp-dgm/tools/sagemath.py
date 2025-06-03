import subprocess
import tempfile
import os
from pathlib import Path

def tool_info():
    return {
        "name": "sagemath",
        "description": """Execute SageMath code for mathematical computations.
        
Capabilities include:
- Number theory computations
- Elliptic curve operations
- Finite field arithmetic
- Polynomial operations
- Linear algebra
- Cryptographic primitives
- Symbolic computation""",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "SageMath code to execute"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default: 60)",
                    "default": 60
                }
            },
            "required": ["code"]
        }
    }

def tool_function(code: str, timeout: int = 60) -> str:
    """Execute SageMath code and return the result."""
    try:
        # Create a temporary file for the SageMath script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sage', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute SageMath
        result = subprocess.run(
            ['sage', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Clean up
        os.unlink(temp_file)
        
        # Prepare output
        output = []
        if result.stdout:
            output.append("Output:")
            output.append(result.stdout)
        if result.stderr:
            output.append("Errors:")
            output.append(result.stderr)
        
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        return f"Error: SageMath execution timed out after {timeout} seconds"
    except Exception as e:
        return f"Error executing SageMath: {str(e)}"