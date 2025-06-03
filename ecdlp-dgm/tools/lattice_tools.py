def tool_info():
    return {
        "name": "lattice_tools",
        "description": """Lattice-based algorithms for cryptanalysis.
        
Algorithms:
- LLL reduction
- BKZ reduction
- CVP/SVP solving
- Coppersmith's method""",
        "input_schema": {
            "type": "object",
            "properties": {
                "algorithm": {
                    "type": "string",
                    "enum": ["lll", "bkz", "cvp", "svp", "coppersmith"],
                    "description": "Lattice algorithm to apply"
                },
                "matrix": {
                    "type": "array",
                    "description": "Lattice basis matrix"
                },
                "params": {
                    "type": "object",
                    "description": "Additional parameters"
                }
            },
            "required": ["algorithm"]
        }
    }

def tool_function(algorithm: str, matrix: list = None, params: dict = None) -> str:
    """Execute lattice algorithms."""
    if params is None:
        params = {}
    
    if matrix is None:
        # Default test matrix
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    sage_code = f"""
# Lattice algorithm: {algorithm}
M = Matrix({matrix})
print(f"Original matrix:\\n{{M}}")

if algorithm == "lll":
    M_reduced = M.LLL()
    print(f"\\nLLL-reduced matrix:\\n{{M_reduced}}")
    print(f"\\nDeterminant: {{M_reduced.det()}}")
elif algorithm == "bkz":
    block_size = {params.get('block_size', 20)}
    M_reduced = M.BKZ(block_size=block_size)
    print(f"\\nBKZ-reduced matrix (block size {{block_size}}):\\n{{M_reduced}}")
"""
    
    from .sagemath import tool_function as sage_exec
    return sage_exec(sage_code)