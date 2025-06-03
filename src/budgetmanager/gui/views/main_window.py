#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Module for the main application window class with a left-side menu.

This module defines the MainWindow class, inheriting from BaseWindow,
and provides a left-hand menu to switch between different tab frames.
"""

# Standard library imports
import tkinter as tk
from typing import Type

# Local application imports
from ..base import BaseWindow


class MainWindow(BaseWindow):
    """
    Main application window with a left-side navigation menu.

    Provides methods to register separate tab frames and switch
    between them via menu buttons.

    Attributes:
        menu_frame (tk.Frame): Container for navigation buttons.
        container (tk.Frame): Container for tab frames.
        tabs (dict[str, tk.Frame]): Mapping of tab name to frame instance.
        buttons (dict[str, tk.Button]): Mapping of tab name to menu button.
    """

    def __init__(self, title: str | None = None) -> None:
        """Initialize the main window and set up layout."""
        super().__init__(title)
        self.tabs: dict[str, tk.Frame] = {}
        self.buttons: dict[str, tk.Button] = {}
        self._setup_frames()

    def _setup_frames(self) -> None:
        """
        Create and grid the menu and container frames.

        The menu_frame holds navigation buttons on the left, and
        the container holds the actual tab frames on the right.
        """
        # Configure grid: column 0 = menu (fixed), column 1 = content (expand)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left-side menu frame
        self.menu_frame: tk.Frame = tk.Frame(self, bd=1, relief="raised")
        self.menu_frame.grid(row=0, column=0, sticky="ns")

        # Right-side container for tab frames
        self.container: tk.Frame = tk.Frame(self)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def register_tab(self, name: str, frame_class: Type[tk.Frame]) -> None:
        """
        Register a new tab frame under the given name.

        Instantiates the frame_class with parent=self.container,
        grids it (initially hidden), and adds a button in the menu.

        Args:
            name (str): Display name of the tab in the menu.
            frame_class (Type[tk.Frame]): Class of the frame to instantiate.
        """
        # Instantiate the frame inside the container
        frame: tk.Frame = frame_class(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_remove()  # Hide until selected

        # Store reference
        self.tabs[name] = frame

        # Create and pack the menu button
        btn: tk.Button = tk.Button(
            self.menu_frame,
            text=name,
            command=lambda n=name: self.show_tab(n),
            anchor="w",
        )
        btn.pack(fill="x", padx=5, pady=2)
        self.buttons[name] = btn

        # If this is the first tab registered, show it by default
        if len(self.tabs) == 1:
            self.show_tab(name)

    def show_tab(self, name: str) -> None:
        """
        Display the tab frame corresponding to the given name.

        Hides all other frames and highlights the active menu button.

        Args:
            name (str): Name of the tab to display.
        """
        for tab_name, frame in self.tabs.items():
            if tab_name == name:
                frame.grid()
                self.buttons[tab_name].config(relief="sunken")
            else:
                frame.grid_remove()
                self.buttons[tab_name].config(relief="raised")
