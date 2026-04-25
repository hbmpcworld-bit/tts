"""
Helper utilities for the TikTok Content Automation Tool
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_api_key(service):
    """Get API key from environment variables"""
    key_map = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'replicate': 'REPLICATE_API_KEY',
        'stability': 'STABILITY_API_KEY'
    }

    key = os.getenv(key_map.get(service, ''))
    if not key:
        raise ValueError(f"API key for {service} not found. Please set {key_map.get(service)} in .env file")
    return key


def save_json(data, filepath):
    """Save data as JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath):
    """Load data from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_timestamp():
    """Get current timestamp for filenames"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_output_dirs():
    """Ensure output directories exist"""
    dirs = ['output/scripts', 'output/images', 'output/videos']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def sanitize_filename(name):
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name[:100]  # Limit length
