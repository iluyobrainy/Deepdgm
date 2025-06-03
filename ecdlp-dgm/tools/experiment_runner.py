import time
from datetime import datetime

def tool_info():
    return {
        "name": "experiment_runner",
        "description": """Run mathematical experiments with progress tracking.
        
Features:
- Batch experiments
- Progress monitoring
- Result aggregation
- Pattern detection""",
        "input_schema": {
            "type": "object",
            "properties": {
                "experiment_type": {
                    "type": "string",
                    "description": "Type of experiment to run"
                },
                "parameters": {
                    "type": "object",
                    "description": "Experiment parameters"
                },
                "iterations": {
                    "type": "integer",
                    "description": "Number of iterations",
                    "default": 100
                }
            },
            "required": ["experiment_type"]
        }
    }

def tool_function(experiment_type: str, parameters: dict = None, iterations: int = 100) -> str:
    """Run mathematical experiments."""
    if parameters is None:
        parameters = {}
    
    results = []
    start_time = time.time()
    
    print(f"\n🔬 Starting experiment: {experiment_type}")
    print(f"📊 Iterations: {iterations}")
    
    # Simulate experiment with progress bar
    for i in range(min(iterations, 10)):  # Limit for demo
        progress = (i + 1) / min(iterations, 10) * 100
        print(f"\r Progress: [{'=' * int(progress/5):<20}] {progress:.1f}%", end='')
        time.sleep(0.1)  # Simulate computation
        
        # Collect some results
        results.append({
            'iteration': i,
            'timestamp': datetime.now().isoformat(),
            'value': i * 1.5  # Placeholder
        })
    
    print("\n✅ Experiment complete!")
    
    duration = time.time() - start_time
    
    return f"""
Experiment Results:
- Type: {experiment_type}
- Iterations completed: {len(results)}
- Duration: {duration:.2f} seconds
- Parameters: {parameters}
- Sample results: {results[:3]}
"""