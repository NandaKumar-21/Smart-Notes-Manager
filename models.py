"""
models.py - Data models for Smart Notes Manager.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Note:
    """Represents a single note with metadata."""

    title: str
    content: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modified_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d%H%M%S%f"))

    def update_content(self, title: str, content: str) -> None:
        """Update the note's title and content, refreshing the modified timestamp."""
        self.title = title
        self.content = content
        self.modified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Serialize the note to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """Deserialize a note from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            created_at=data["created_at"],
            modified_at=data["modified_at"],
        )
