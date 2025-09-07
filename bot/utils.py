import json
import os

# Get the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construct the absolute path to config.json
config_path = os.path.join(project_root, 'config.json')

def load_config():
    """Loads the configuration from config.json."""
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config):
    """Saves the configuration to config.json."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
