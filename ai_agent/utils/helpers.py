"""
Helper utility functions
"""

import json
import os
import time
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from pathlib import Path


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if it doesn't"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """Save data to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().isoformat()


def format_elapsed_time(start_time: float) -> str:
    """Format elapsed time from start time"""
    elapsed = time.time() - start_time
    if elapsed < 1:
        return f"{elapsed*1000:.0f}ms"
    elif elapsed < 60:
        return f"{elapsed:.1f}s"
    else:
        minutes = int(elapsed // 60)
        seconds = elapsed % 60
        return f"{minutes}m {seconds:.1f}s"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with default"""
    return dictionary.get(key, default)


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def validate_api_key(api_key: Optional[str]) -> bool:
    """Validate API key format"""
    if not api_key:
        return False
    
    # Basic validation - should be a non-empty string
    if not isinstance(api_key, str) or len(api_key.strip()) == 0:
        return False
    
    # Should not contain spaces
    if ' ' in api_key:
        return False
    
    return True


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem safety"""
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename


def count_tokens_approximate(text: str) -> int:
    """Approximate token count (rough estimation)"""
    # Simple approximation: 1 token ≈ 4 characters for English text
    # This is a very rough estimate and should be replaced with proper tokenization
    return len(text) // 4


def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown text"""
    import re
    
    # Pattern to match code blocks
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    code_blocks = []
    for language, code in matches:
        code_blocks.append({
            'language': language or 'text',
            'code': code.strip()
        })
    
    return code_blocks


def format_model_name(model_name: str) -> str:
    """Format model name for display"""
    # Convert model identifiers to readable names
    model_display_names = {
        'gpt-4': 'GPT-4',
        'gpt-4-turbo': 'GPT-4 Turbo',
        'gpt-3.5-turbo': 'GPT-3.5 Turbo',
        'gpt-4o': 'GPT-4o',
        'gpt-4o-mini': 'GPT-4o Mini',
        'claude-3-opus-20240229': 'Claude 3 Opus',
        'claude-3-sonnet-20240229': 'Claude 3 Sonnet',
        'claude-3-haiku-20240307': 'Claude 3 Haiku',
        'claude-3-5-sonnet-20241022': 'Claude 3.5 Sonnet',
    }
    
    return model_display_names.get(model_name, model_name)
