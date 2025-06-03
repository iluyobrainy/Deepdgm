import datetime
import json
import os
from pathlib import Path

from llm import create_client, get_response_from_llm, extract_json_between_markers
from utils.common_utils import load_json_file, save_json_file

def self_improve(
    parent_commit='initial',
    output_dir='output_selfimprove/',
    entry='number_theory_deep_dive',
    test_task_list=None
):
    """Self-improvement step for mathematical research."""
    
    # Create output directory
    run_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    output_path = Path(output_dir) / run_id
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create metadata
    metadata = {
        'run_id': run_id,
        'parent_commit': parent_commit,
        'entry': entry,
        'start_time': datetime.datetime.now().isoformat()
    }
    
    # Get improvement suggestions
    print(f"Running self-improvement for: {entry}")
    
    # Analyze current capabilities
    prompt = f"""Analyze the mathematical research agent's approach to ECDLP and suggest improvements.

Focus area: {entry}

Provide specific improvements for:
1. Mathematical tools and techniques
2. Research strategies
3. Verification methods
4. Exploration patterns

Format your response as JSON with these fields:
- analysis: Current approach analysis
- improvements: List of specific improvements
- implementation: How to implement the top improvement
"""
    
    client = create_client('deepseek-r1-0528')
    response, _ = get_response_from_llm(
        msg=prompt,
        client=client[0],
        model=client[1],
        system_message="You are an expert in mathematical research and AI systems.",
        temperature=0.7
    )
    
    # Extract improvements
    improvements = extract_json_between_markers(response)
    if improvements:
        metadata['suggested_improvements'] = improvements
        
        # Generate patch based on top improvement
        top_improvement = improvements.get('improvements', [{}])[0]
        metadata['implemented_improvement'] = top_improvement
    
    # Save metadata
    save_json_file(metadata, output_path / 'metadata.json')
    
    # Create a simple model patch (in real implementation, this would modify code)
    model_patch = f"""# Self-improvement patch
# Focus: {entry}
# Timestamp: {run_id}

# Improvements would be implemented here
"""
    
    with open(output_path / 'model_patch.diff', 'w') as f:
        f.write(model_patch)
    
    print(f"Self-improvement complete. Results in: {output_path}")
    return metadata