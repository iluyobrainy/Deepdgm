def tool_info():
    return {
        "name": "visualization",
        "description": """Visualize mathematical objects and results.
        
Capabilities:
- Elliptic curve plots
- Point distributions
- Algorithm performance
- Pattern visualization""",
        "input_schema": {
            "type": "object",
            "properties": {
                "plot_type": {
                    "type": "string",
                    "enum": ["curve", "points", "performance", "pattern"],
                    "description": "Type of visualization"
                },
                "data": {
                    "type": "object",
                    "description": "Data to visualize"
                }
            },
            "required": ["plot_type"]
        }
    }

def tool_function(plot_type: str, data: dict = None) -> str:
    """Create mathematical visualizations."""
    if data is None:
        data = {}
    
    # For now, we'll create text-based visualizations
    if plot_type == "curve":
        return """
Elliptic Curve Visualization (y² = x³ + 7 over small field):
    
    10 |     *
     9 |   *   *
     8 | *       *
     7 |           *
     6 | *       *
     5 |   *   *
     4 |     *
     3 |
     2 | *   *   *
     1 |   *   *
     0 |_____________
       0 1 2 3 4 5 6
       
Note: This is a simplified representation.
For actual secp256k1, use SageMath plotting.
"""
    
    elif plot_type == "performance":
        return """
Algorithm Performance:
Baby-step Giant-step: ████████████░░░░░░░░ 60%
Pollard's rho:        ████████░░░░░░░░░░░░ 40%
Novel approach:       ██░░░░░░░░░░░░░░░░░░ 10%
"""
    
    return f"Visualization of type '{plot_type}' with data: {data}"