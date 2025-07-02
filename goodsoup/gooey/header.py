#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# gui/header.py
"""



import tkinter as tk
from gooey.instructions import open_instructions_window

class Header(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#084b39')  # Header background color
        self.controller = controller
        self.configure(padx=10, pady=10)

        home_btn = tk.Button(
            self,
            text="Home",
            bg='#f7b4c6',
            fg='#000000',
            activebackground='#d9a8b2',
            activeforeground='#000000',
            command=lambda: controller.show_frame("StartPage")
        )
        home_btn.pack(side=tk.LEFT, padx=(0, 10))

        instructions_btn = tk.Button(
            self,
            text="Instructions",
            bg='#f7b4c6',
            fg='#000000',
            activebackground='#d9a8b2',
            activeforeground='#000000',
            command=open_instructions_window
        )
        instructions_btn.pack(side=tk.RIGHT)