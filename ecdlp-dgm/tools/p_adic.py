def tool_info():
    return {
        "name": "p_adic",
        "description": """p-adic number analysis for ECDLP research.
        
Operations:
- p-adic valuations
- p-adic logarithms
- Local field computations
- Hensel lifting""",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["valuation", "logarithm", "hensel_lift", "local_analysis"],
                    "description": "p-adic operation to perform"
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
    """Execute p-adic computations."""
    prime = params.get('prime', 2)
    value = params.get('value', 1)
    
    sage_code = f"""
# p-adic computation
p = {prime}
Qp = pAdicField(p, prec=20)

if operation == "valuation":
    x = Qp({value})
    result = x.valuation()
    print(f"p-adic valuation of {value} with respect to prime {{p}}: {{result}}")
elif operation == "logarithm":
    # p-adic logarithm computation
    x = Qp({value})
    if x.valuation() > 0:
        result = x.log()
        print(f"p-adic logarithm: {{result}}")
    else:
        print("p-adic logarithm not defined for this value")
"""
    
    from .sagemath import tool_function as sage_exec
    return sage_exec(sage_code)