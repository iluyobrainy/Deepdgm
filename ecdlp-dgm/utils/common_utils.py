import json
from pathlib import Path

def read_file(file_path):
    """Read a file and return its contents."""
    with open(file_path, 'r') as f:
        return f.read().strip()

def load_json_file(file_path):
    """Load a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json_file(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def ensure_dir(path):
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)