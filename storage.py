"""
storage.py - JSON persistence layer for Smart Notes Manager.
"""

import json
import os
from typing import List

from models import Note

NOTES_FILE = "notes.json"


class NoteStorage:
    """Handles reading and writing notes to a JSON file."""

    def __init__(self, filepath: str = NOTES_FILE) -> None:
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the JSON file with an empty list if it does not exist."""
        if not os.path.exists(self.filepath):
            self._write([])

    def _read(self) -> List[dict]:
        """Read raw note dictionaries from the JSON file."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    def _write(self, data: List[dict]) -> None:
        """Write raw note dictionaries to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_all(self) -> List[Note]:
        """Load and return all notes from storage."""
        return [Note.from_dict(d) for d in self._read()]

    def save_all(self, notes: List[Note]) -> None:
        """Persist all notes to storage."""
        self._write([note.to_dict() for note in notes])
