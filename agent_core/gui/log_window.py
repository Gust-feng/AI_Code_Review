"""Minimal log viewer window attached to the main GUI."""

from __future__ import annotations

import tkinter as tk
from queue import Empty

from agent_core.infrastructure.logging.gui_handler import GuiLogHandler
from agent_core.infrastructure.logging.logger import logger


class LogWindow:
    """Small background GUI that streams structured logs."""

    def __init__(self, master: tk.Tk, title: str = "Agent Logs") -> None:
        self._handler = GuiLogHandler()
        logger.addHandler(self._handler)

        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.geometry("520x280")
        self.top.configure(bg="#1e1e1e")
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)
        self.text = tk.Text(
            self.top,
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            wrap=tk.NONE,
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.configure(state=tk.DISABLED)
        self._poll()

    def _poll(self) -> None:
        queue = self._handler.get_queue()
        appended = False
        while True:
            try:
                line = queue.get_nowait()
            except Empty:
                break
            appended = True
            self.text.configure(state=tk.NORMAL)
            self.text.insert(tk.END, line + "\n")
            self.text.configure(state=tk.DISABLED)
            self.text.see(tk.END)
        if self.top.winfo_exists():
            self.top.after(300, self._poll)
        elif appended:
            queue.queue.clear()

    def _on_close(self) -> None:
        logger.removeHandler(self._handler)
        self.top.destroy()
