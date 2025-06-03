#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Module for the GUI base window and tab classes using Tkinter.

This module defines the BaseWindow class, which serves as a base
for all GUI windows, and the BaseTab class, which serves as a base
for all tab frames in the BudgetManager application.
"""

import tkinter as tk


class BaseWindow(tk.Tk):
    """
    A base class for Tkinter windows providing common setup.

    Args:
        title (str | None): Optional window title. If provided, sets the
            window's title.

    Attributes:
        title (str | None): Title of the window.
    """

    def __init__(self, title: str | None = None) -> None:
        """Initialize the base window and configure default settings.

        Args:
            title (str | None): Optional window title.
        """
        super().__init__()
        if title:
            self.title(title)
        self._configure_window()

    def _configure_window(self) -> None:
        """
        Configure default window settings, such as minimum size
        and default padding. Subclasses can override this method to
        customize window appearance and behavior.
        """
        self.minsize(800, 600)

    def run(self) -> None:
        """
        Start the Tkinter main event loop to display the window.

        This method should be called after all widgets have been added.
        """
        self.mainloop()


class BaseTab(tk.Frame):
    """
    A base class for tab frames in Tkinter windows providing common setup.

    Args:
        parent (tk.Widget): Parent container for the tab.

    Attributes:
        parent (tk.Widget): The parent widget.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the base tab frame.

        Args:
            parent (tk.Widget): Parent container for the tab.
        """
        super().__init__(parent)
        self.parent = parent
        self._configure_tab()

    def _configure_tab(self) -> None:
        """
        Configure default tab settings. Subclasses can override
        to customize appearance and behavior of the tab.
        """
        # Default implementation does nothing. Subclasses may override.
        pass

    def on_show(self) -> None:
        """
        Called when the tab is shown. Subclasses can override to
        refresh or update contents.
        """
        # Default implementation does nothing. Subclasses may override.
        pass

    def on_hide(self) -> None:
        """
        Called when the tab is hidden. Subclasses can override to
        perform cleanup or state saving.
        """
        # Default implementation does nothing. Subclasses may override.
        pass
