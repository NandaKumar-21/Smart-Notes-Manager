"""
gui.py - Main application window and UI logic for Smart Notes Manager.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List, Optional

from models import Note
from storage import NoteStorage
from utils import THEMES, truncate, validate_note


class SmartNotesApp(tk.Tk):
    """Root application window for Smart Notes Manager."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Smart Notes Manager")
        self.geometry("1000x650")
        self.minsize(800, 550)

        self._storage = NoteStorage()
        self._notes: List[Note] = self._storage.load_all()
        self._filtered_notes: List[Note] = list(self._notes)
        self._selected_note: Optional[Note] = None
        self._current_theme: str = "dark"
        self._auto_save_job: Optional[str] = None
        self._is_new_note: bool = False

        self._build_ui()
        self._apply_theme()
        self._refresh_list()
        self._bind_shortcuts()
        self._update_status()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct all UI widgets."""
        self._build_toolbar()
        self._build_main_area()
        self._build_status_bar()

    def _build_toolbar(self) -> None:
        """Build the top toolbar with action buttons and search."""
        self._toolbar = tk.Frame(self, height=50)
        self._toolbar.pack(side=tk.TOP, fill=tk.X)
        self._toolbar.pack_propagate(False)

        btn_cfg = {"relief": tk.FLAT, "cursor": "hand2", "padx": 12, "pady": 6, "font": ("Segoe UI", 10)}

        self._btn_new = tk.Button(self._toolbar, text="+ New Note", command=self._new_note, **btn_cfg)
        self._btn_new.pack(side=tk.LEFT, padx=(10, 4), pady=6)

        self._btn_save = tk.Button(self._toolbar, text="Save", command=self._save_note, **btn_cfg)
        self._btn_save.pack(side=tk.LEFT, padx=4, pady=6)

        self._btn_delete = tk.Button(self._toolbar, text="Delete", command=self._delete_note, **btn_cfg)
        self._btn_delete.pack(side=tk.LEFT, padx=4, pady=6)

        self._btn_theme = tk.Button(self._toolbar, text="Light Mode", command=self._toggle_theme, **btn_cfg)
        self._btn_theme.pack(side=tk.RIGHT, padx=(4, 10), pady=6)

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)
        self._search_entry = tk.Entry(
            self._toolbar,
            textvariable=self._search_var,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            width=28,
        )
        self._search_entry.pack(side=tk.RIGHT, padx=4, pady=10, ipady=4)

        self._lbl_search = tk.Label(self._toolbar, text="Search:", font=("Segoe UI", 10))
        self._lbl_search.pack(side=tk.RIGHT, padx=(8, 0))

    def _build_main_area(self) -> None:
        """Build the sidebar notes list and the editor panel."""
        self._paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=4, sashrelief=tk.FLAT)
        self._paned.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar()
        self._build_editor()

    def _build_sidebar(self) -> None:
        """Build the scrollable notes list in the sidebar."""
        sidebar = tk.Frame(self._paned, width=260)
        sidebar.pack_propagate(False)
        self._paned.add(sidebar, minsize=180)
        self._sidebar_frame = sidebar

        self._lbl_notes_heading = tk.Label(sidebar, text="Notes", font=("Segoe UI", 11, "bold"), anchor="w")
        self._lbl_notes_heading.pack(fill=tk.X, padx=12, pady=(10, 4))

        list_frame = tk.Frame(sidebar)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self._notes_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            activestyle="none",
            cursor="hand2",
        )
        scrollbar.config(command=self._notes_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._notes_listbox.bind("<<ListboxSelect>>", self._on_note_select)
        self._notes_listbox.bind("<Delete>", lambda _: self._delete_note())

    def _build_editor(self) -> None:
        """Build the note editor panel on the right side."""
        editor_frame = tk.Frame(self._paned)
        self._paned.add(editor_frame, minsize=400)
        self._editor_frame = editor_frame

        meta_frame = tk.Frame(editor_frame)
        meta_frame.pack(fill=tk.X, padx=16, pady=(12, 4))

        self._lbl_created = tk.Label(meta_frame, text="", font=("Segoe UI", 8), anchor="w")
        self._lbl_created.pack(side=tk.LEFT)

        self._lbl_modified = tk.Label(meta_frame, text="", font=("Segoe UI", 8), anchor="e")
        self._lbl_modified.pack(side=tk.RIGHT)

        self._title_var = tk.StringVar()
        self._title_entry = tk.Entry(
            editor_frame,
            textvariable=self._title_var,
            font=("Segoe UI", 14, "bold"),
            relief=tk.FLAT,
            borderwidth=0,
        )
        self._title_entry.pack(fill=tk.X, padx=16, pady=(0, 6), ipady=6)
        self._title_var.trace_add("write", self._on_content_change)

        separator = tk.Frame(editor_frame, height=1)
        separator.pack(fill=tk.X, padx=16)
        self._separator = separator

        text_frame = tk.Frame(editor_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(8, 0))

        text_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        self._content_text = tk.Text(
            text_frame,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            borderwidth=0,
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            undo=True,
        )
        text_scroll.config(command=self._content_text.yview)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._content_text.bind("<<Modified>>", self._on_text_modified)

        bottom_bar = tk.Frame(editor_frame)
        bottom_bar.pack(fill=tk.X, padx=16, pady=(4, 8))

        self._lbl_char_count = tk.Label(bottom_bar, text="0 characters", font=("Segoe UI", 8), anchor="e")
        self._lbl_char_count.pack(side=tk.RIGHT)

    def _build_status_bar(self) -> None:
        """Build the bottom status bar."""
        self._status_bar = tk.Frame(self, height=26)
        self._status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._status_bar.pack_propagate(False)

        self._lbl_status = tk.Label(
            self._status_bar, text="", font=("Segoe UI", 9), anchor="w"
        )
        self._lbl_status.pack(side=tk.LEFT, padx=12)

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------

    def _apply_theme(self) -> None:
        """Apply the current theme colours to all widgets."""
        t = THEMES[self._current_theme]

        self.configure(bg=t["bg"])
        self._toolbar.configure(bg=t["sidebar_bg"])
        self._status_bar.configure(bg=t["status_bg"])
        self._lbl_status.configure(bg=t["status_bg"], fg=t["subtext"])
        self._paned.configure(bg=t["border"])

        for btn in (self._btn_new, self._btn_save, self._btn_delete, self._btn_theme):
            btn.configure(bg=t["button_bg"], fg=t["button_fg"], activebackground=t["select_bg"], activeforeground=t["text"])

        self._lbl_search.configure(bg=t["sidebar_bg"], fg=t["subtext"])
        self._search_entry.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["text"])

        self._sidebar_frame.configure(bg=t["sidebar_bg"])
        self._lbl_notes_heading.configure(bg=t["sidebar_bg"], fg=t["text"])
        self._notes_listbox.configure(
            bg=t["sidebar_bg"],
            fg=t["text"],
            selectbackground=t["select_bg"],
            selectforeground=t["select_fg"],
        )

        self._editor_frame.configure(bg=t["panel_bg"])
        self._lbl_created.configure(bg=t["panel_bg"], fg=t["subtext"])
        self._lbl_modified.configure(bg=t["panel_bg"], fg=t["subtext"])
        self._title_entry.configure(bg=t["panel_bg"], fg=t["text"], insertbackground=t["text"])
        self._separator.configure(bg=t["border"])
        self._content_text.configure(
            bg=t["panel_bg"],
            fg=t["text"],
            insertbackground=t["text"],
            selectbackground=t["select_bg"],
            selectforeground=t["select_fg"],
        )
        self._lbl_char_count.configure(bg=t["panel_bg"], fg=t["subtext"])

        for child in self._editor_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=t["panel_bg"])

        self._btn_theme.configure(text="Light Mode" if self._current_theme == "dark" else "Dark Mode")

    def _toggle_theme(self) -> None:
        """Switch between dark and light themes."""
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        self._apply_theme()

    # ------------------------------------------------------------------
    # Notes List Management
    # ------------------------------------------------------------------

    def _refresh_list(self) -> None:
        """Repopulate the listbox from the filtered notes list."""
        self._notes_listbox.delete(0, tk.END)
        for note in self._filtered_notes:
            self._notes_listbox.insert(tk.END, f"  {truncate(note.title)}")

        if self._selected_note:
            self._reselect_in_list()

    def _reselect_in_list(self) -> None:
        """Highlight the currently selected note in the listbox."""
        for i, note in enumerate(self._filtered_notes):
            if note.id == self._selected_note.id:
                self._notes_listbox.selection_clear(0, tk.END)
                self._notes_listbox.selection_set(i)
                self._notes_listbox.see(i)
                return

    def _on_note_select(self, _event: tk.Event) -> None:
        """Handle listbox selection change."""
        selection = self._notes_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self._filtered_notes):
            self._load_note_into_editor(self._filtered_notes[index])

    def _load_note_into_editor(self, note: Note) -> None:
        """Populate the editor fields with the given note's data."""
        self._selected_note = note
        self._is_new_note = False

        self._title_var.set(note.title)

        self._content_text.config(state=tk.NORMAL)
        self._content_text.delete("1.0", tk.END)
        self._content_text.insert("1.0", note.content)
        self._content_text.edit_modified(False)

        self._lbl_created.configure(text=f"Created: {note.created_at}")
        self._lbl_modified.configure(text=f"Modified: {note.modified_at}")
        self._update_char_count()

    # ------------------------------------------------------------------
    # CRUD Operations
    # ------------------------------------------------------------------

    def _new_note(self) -> None:
        """Prepare the editor for creating a new note."""
        self._selected_note = None
        self._is_new_note = True
        self._notes_listbox.selection_clear(0, tk.END)

        self._title_var.set("")
        self._content_text.delete("1.0", tk.END)
        self._content_text.edit_modified(False)
        self._lbl_created.configure(text="")
        self._lbl_modified.configure(text="")
        self._lbl_char_count.configure(text="0 characters")
        self._title_entry.focus_set()

    def _save_note(self) -> None:
        """Validate and persist the current editor contents."""
        title = self._title_var.get().strip()
        content = self._content_text.get("1.0", tk.END).strip()

        error = validate_note(title, content)
        if error:
            messagebox.showerror("Validation Error", error, parent=self)
            return

        if self._is_new_note or self._selected_note is None:
            note = Note(title=title, content=content)
            self._notes.append(note)
            self._selected_note = note
            self._is_new_note = False
        else:
            self._selected_note.update_content(title, content)
            self._lbl_modified.configure(text=f"Modified: {self._selected_note.modified_at}")

        self._storage.save_all(self._notes)
        self._apply_search_filter()
        self._refresh_list()
        self._update_status()
        self._content_text.edit_modified(False)
        messagebox.showinfo("Saved", "Note saved successfully.", parent=self)

    def _delete_note(self) -> None:
        """Delete the selected note after confirmation."""
        if self._selected_note is None:
            messagebox.showwarning("No Selection", "Please select a note to delete.", parent=self)
            return

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f'Are you sure you want to delete "{self._selected_note.title}"?',
            parent=self,
        )
        if not confirmed:
            return

        self._notes = [n for n in self._notes if n.id != self._selected_note.id]
        self._storage.save_all(self._notes)
        self._selected_note = None
        self._is_new_note = False

        self._title_var.set("")
        self._content_text.delete("1.0", tk.END)
        self._lbl_created.configure(text="")
        self._lbl_modified.configure(text="")
        self._lbl_char_count.configure(text="0 characters")

        self._apply_search_filter()
        self._refresh_list()
        self._update_status()

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def _on_search_change(self, *_args) -> None:
        """Triggered on every keystroke in the search field."""
        self._apply_search_filter()
        self._refresh_list()

    def _apply_search_filter(self) -> None:
        """Filter the notes list based on the current search query."""
        query = self._search_var.get().strip().lower()
        if not query:
            self._filtered_notes = list(self._notes)
        else:
            self._filtered_notes = [
                n for n in self._notes
                if query in n.title.lower() or query in n.content.lower()
            ]

    def _focus_search(self) -> None:
        """Move keyboard focus to the search entry."""
        self._search_entry.focus_set()

    # ------------------------------------------------------------------
    # Auto-save
    # ------------------------------------------------------------------

    def _on_content_change(self, *_args) -> None:
        """Schedule an auto-save when the title changes."""
        self._schedule_auto_save()

    def _on_text_modified(self, _event: tk.Event) -> None:
        """Handle Text widget modification flag."""
        if self._content_text.edit_modified():
            self._update_char_count()
            self._schedule_auto_save()
            self._content_text.edit_modified(False)

    def _schedule_auto_save(self) -> None:
        """Debounce auto-save: save 2 seconds after the last change."""
        if self._auto_save_job:
            self.after_cancel(self._auto_save_job)
        self._auto_save_job = self.after(2000, self._auto_save)

    def _auto_save(self) -> None:
        """Silently save the current note without showing a dialog."""
        title = self._title_var.get().strip()
        content = self._content_text.get("1.0", tk.END).strip()

        if not title or not content:
            return

        if self._is_new_note or self._selected_note is None:
            note = Note(title=title, content=content)
            self._notes.append(note)
            self._selected_note = note
            self._is_new_note = False
        else:
            self._selected_note.update_content(title, content)
            self._lbl_modified.configure(text=f"Modified: {self._selected_note.modified_at}")

        self._storage.save_all(self._notes)
        self._apply_search_filter()
        self._refresh_list()
        self._update_status()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _update_char_count(self) -> None:
        """Refresh the character counter label."""
        count = len(self._content_text.get("1.0", tk.END)) - 1  # subtract trailing newline
        self._lbl_char_count.configure(text=f"{count} character{'s' if count != 1 else ''}")

    def _update_status(self) -> None:
        """Refresh the status bar note count."""
        total = len(self._notes)
        self._lbl_status.configure(text=f"{total} note{'s' if total != 1 else ''} total")

    def _bind_shortcuts(self) -> None:
        """Register global keyboard shortcuts."""
        self.bind_all("<Control-n>", lambda _: self._new_note())
        self.bind_all("<Control-s>", lambda _: self._save_note())
        self.bind_all("<Control-f>", lambda _: self._focus_search())
