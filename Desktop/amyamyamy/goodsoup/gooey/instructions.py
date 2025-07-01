#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weekly sale
"""

import tkinter as tk
from tkinter import ttk

def open_instructions_window():
    instructions_win = tk.Toplevel()
    instructions_win.title("Instructions")
    instructions_win.geometry("400x300")

    label = ttk.Label(instructions_win, text="Instructions go here.", font=("Helvetica", 12))
    label.pack(pady=20)

    close_btn = ttk.Button(instructions_win, text="Close", command=instructions_win.destroy)
    close_btn.pack(pady=10)