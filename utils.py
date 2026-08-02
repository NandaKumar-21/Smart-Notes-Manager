"""
utils.py - Utility helpers and theme definitions for Smart Notes Manager.
"""

from typing import Dict

THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        "bg": "#1e1e2e",
        "sidebar_bg": "#181825",
        "panel_bg": "#1e1e2e",
        "text": "#cdd6f4",
        "subtext": "#a6adc8",
        "accent": "#89b4fa",
        "accent_hover": "#74c7ec",
        "entry_bg": "#313244",
        "entry_fg": "#cdd6f4",
        "select_bg": "#45475a",
        "select_fg": "#cdd6f4",
        "border": "#45475a",
        "button_bg": "#313244",
        "button_fg": "#cdd6f4",
        "danger": "#f38ba8",
        "success": "#a6e3a1",
        "status_bg": "#181825",
    },
    "light": {
        "bg": "#eff1f5",
        "sidebar_bg": "#e6e9ef",
        "panel_bg": "#eff1f5",
        "text": "#4c4f69",
        "subtext": "#6c6f85",
        "accent": "#1e66f5",
        "accent_hover": "#04a5e5",
        "entry_bg": "#dce0e8",
        "entry_fg": "#4c4f69",
        "select_bg": "#bcc0cc",
        "select_fg": "#4c4f69",
        "border": "#bcc0cc",
        "button_bg": "#dce0e8",
        "button_fg": "#4c4f69",
        "danger": "#d20f39",
        "success": "#40a02b",
        "status_bg": "#e6e9ef",
    },
}


def truncate(text: str, max_length: int = 45) -> str:
    """Return text truncated with an ellipsis if it exceeds max_length."""
    return text if len(text) <= max_length else text[:max_length].rstrip() + "..."


def validate_note(title: str, content: str) -> str:
    """
    Validate note fields.

    Returns an error message string if invalid, or an empty string if valid.
    """
    if not title.strip():
        return "Title cannot be empty."
    if not content.strip():
        return "Content cannot be empty."
    return ""
