"""
Helper utilities for the Legal Expert System.
Common functions used across the application.
"""
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def load_json_file(filepath):
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in {filepath}: {e}")
        return None


def save_json_file(filepath, data):
    """Save data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {filepath}: {e}")
        return False


def format_datetime(dt=None):
    """Format datetime for display."""
    if dt is None:
        dt = datetime.now()
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def format_date(dt=None):
    """Format date only for display."""
    if dt is None:
        dt = datetime.now()
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime("%d/%m/%Y")


def truncate_text(text, max_length=100):
    """Truncate text to max_length with ellipsis."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_score(score, decimal_places=1):
    """Format a numeric score for display."""
    return f"{score:.{decimal_places}f}"


def validate_input_range(value, min_val, max_val, name=""):
    """Validate that a value is within the expected range."""
    try:
        value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Giá trị '{name}' không hợp lệ: {value}")
    if value < min_val or value > max_val:
        raise ValueError(
            f"Giá trị '{name}' phải nằm trong khoảng [{min_val}, {max_val}]"
        )
    return value
