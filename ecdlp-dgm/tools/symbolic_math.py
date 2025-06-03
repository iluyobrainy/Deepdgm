def tool_info():
    return {
        "name": "symbolic_math",
        "description": "Symbolic mathematics operations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"},
                "operation": {"type": "string"}
            },
            "required": ["expression", "operation"]
        }
    }

def tool_function(expression, operation):
    return f"Symbolic operation {operation} on {expression}"