# Smart Notes Manager

A production-quality desktop notes application built with Python and Tkinter. Designed with clean architecture, OOP principles, and a polished user interface featuring dark and light themes.

## Description

Smart Notes Manager is a fully functional desktop application that allows users to create, edit, search, and delete notes. Notes are persisted locally in a JSON file. The application features auto-save, instant search, character counting, timestamps, keyboard shortcuts, and a toggleable dark/light theme.

## Features

- Create, edit, and delete notes
- Instant search across note titles and content
- Auto-save with 2-second debounce
- JSON-based local storage with automatic file creation
- Character counter in the editor
- Created and last modified timestamps per note
- Confirmation dialog before deleting a note
- Dark mode and light mode with a single click
- Keyboard shortcuts for common actions
- Scrollable notes list in the sidebar
- Status bar showing total note count
- Input validation with error dialogs
- Responsive layout with resizable panes

## Technologies Used

- Python 3.8+
- Tkinter (standard library GUI toolkit)
- ttk (themed Tkinter widgets)
- json (standard library)
- dataclasses (standard library)

No third-party dependencies are required.

## Project Structure

```
Smart-Notes-Manager/
├── main.py           # Application entry point
├── gui.py            # Main window and all UI logic
├── models.py         # Note data model (dataclass)
├── storage.py        # JSON read/write layer
├── utils.py          # Theme definitions and helper functions
├── notes.json        # Persistent note storage (auto-created)
├── requirements.txt  # Dependency notes (stdlib only)
├── README.md
├── LICENSE
├── .gitignore
└── Screenshots/      # Application screenshots
```

## Installation

1. Ensure Python 3.8 or higher is installed.

2. Verify that Tkinter is available:

   ```bash
   python -m tkinter
   ```

   On some Linux distributions, install it with:

   ```bash
   sudo apt-get install python3-tk
   ```

3. Clone the repository:

   ```bash
   git clone https://github.com/NandaKumar-21/Smart-Notes-Manager.git
   cd Smart-Notes-Manager
   ```

No additional packages need to be installed.

## How to Run

```bash
python main.py
```

The application will launch immediately. If `notes.json` does not exist, it will be created automatically on first run.

## Application Screenshots

Screenshots are located in the `Screenshots/` directory.

| Dark Mode | Light Mode |
|-----------|------------|
| ![Dark Mode](Screenshots/dark_mode.png) | ![Light Mode](Screenshots/light_mode.png) |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | Create a new note |
| Ctrl+S | Save the current note |
| Ctrl+F | Focus the search field |
| Delete | Delete the selected note (when list is focused) |

## Learning Outcomes

- Applying OOP and clean architecture principles in a desktop application
- Separating UI logic from business logic and data persistence
- Implementing debounced auto-save using Tkinter's `after` scheduler
- Managing application state across multiple UI components
- Designing a consistent theming system with a single source of truth
- Using Python dataclasses for clean, typed data models
- Handling edge cases and user input validation gracefully

## Future Improvements

- Note categories and tags for better organisation
- Export notes to plain text or Markdown files
- Rich text formatting support in the editor
- Note pinning and sorting options
- Cloud sync via an optional backend API
- Full-text search with highlighted matches
- Configurable auto-save interval

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Nanda Kumar
- GitHub: [https://github.com/NandaKumar-21](https://github.com/NandaKumar-21)

## GitHub Repository

[https://github.com/NandaKumar-21/Smart-Notes-Manager](https://github.com/NandaKumar-21/Smart-Notes-Manager)

## Contribution Guidelines

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear, descriptive messages.
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a pull request describing the changes and the problem they solve.

Please follow PEP 8 coding standards, include type hints, and keep functions small and focused. Avoid introducing third-party dependencies unless absolutely necessary.
