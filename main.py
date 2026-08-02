"""
main.py - Entry point for Smart Notes Manager.
"""

from gui import SmartNotesApp


def main() -> None:
    """Initialize and run the Smart Notes Manager application."""
    app = SmartNotesApp()
    app.mainloop()


if __name__ == "__main__":
    main()
