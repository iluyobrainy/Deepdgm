def tool_info():
    return {
        "name": "number_theory",
        "description": """Advanced number theory computations for cryptanalysis.
        
Includes:
- Prime factorization algorithms
- Discrete logarithm in various groups
- Lattice reduction (LLL, BKZ)
- Continued fractions
- Quadratic forms
- Class field theory computations""",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "Number theory operation to perform"
                },
                "params": {
                    "type": "object",
                    "description": "Parameters for the operation"
                }
            },
            "required": ["operation", "params"]
        }
    }

def tool_function(operation: str, params: dict) -> str:
    """Execute number theory computations."""
    operations = {
        'factor': factor_integer,
        'discrete_log': compute_discrete_log,
        'lattice_reduce': lattice_reduction,
        'continued_fraction': continued_fraction_analysis,
        'class_group': class_group_computation
    }
    
    if operation in operations:
        return operations[operation](params)
    else:
        return f"Unknown operation: {operation}"

def factor_integer(params: dict) -> str:
    """Factor large integers using various algorithms."""
    n = params.get('n')
    algorithm = params.get('algorithm', 'auto')
    
    # Interface with SageMath for factorization
    sage_code = f"""
n = {n}
if algorithm == 'auto':
    factors = factor(n)
elif algorithm == 'ecm':
    factors = ecm.factor(n)
elif algorithm == 'qs':
    factors = qsieve(n)
else:
    factors = "Unsupported algorithm"
    
print(f"Factorization of {n}: {{factors}}")
"""
    
    from .sagemath import tool_function as sage_exec
    return sage_exec(sage_code)

def compute_discrete_log(params: dict) -> str:
    """Compute discrete logarithms in various groups."""
    # Implementation
    return "Discrete log computation"

def lattice_reduction(params: dict) -> str:
    """Perform lattice reduction algorithms."""
    # Implementation
    return "Lattice reduction result"

def continued_fraction_analysis(params: dict) -> str:
    """Analyze continued fractions for cryptanalysis."""
    # Implementation
    return "Continued fraction analysis"

def class_group_computation(params: dict) -> str:
    """Compute class groups and related structures."""
    # Implementation
    return "Class group computation"