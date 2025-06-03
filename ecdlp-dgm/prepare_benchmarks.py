#!/usr/bin/env python3
import json
import os
from pathlib import Path

def create_initial_benchmarks():
    """Create initial ECDLP benchmarks for testing."""
    
    # Create directories
    dirs = [
        "initial/logs",
        "ecdlp_benchmark/test_cases",
        "output_dgm",
        "checkpoints",
        "workspace"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✓ Created directory structure")
    
    # Create initial test cases
    test_cases = {
        "toy_cases": [
            {
                "id": "toy_1",
                "private_key": 12345,
                "public_key": "Calculate using secp256k1",
                "difficulty": "toy"
            }
        ]
    }
    
    with open("ecdlp_benchmark/test_cases/initial_tests.json", "w") as f:
        json.dump(test_cases, f, indent=2)
    
    print("✓ Created initial test cases")
    print("✓ Initial setup complete!")

if __name__ == "__main__":
    create_initial_benchmarks()