#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUBFRAMES OF CREATEGRAPHIC
"""

import tkinter as tk
from tkinter import filedialog
from core.no_gui_main import make_collage
import tkinter as tk
from tkinter import filedialog

class SelectExcelFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f7b4c6")  # Match background
        self.controller = controller  # This should be CreateFlyerPage instance managing steps
        self.selected_file = None

        # Center container
        container = tk.Frame(self, bg="#f7b4c6")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Instruction label
        tk.Label(container, text="Select an Excel file to load", font=("Helvetica", 16), bg="#f7b4c6").pack(pady=20)

        # Browse button
        select_btn = tk.Button(container, text="Browse Excel File...", command=self.browse_file)
        select_btn.pack(pady=10)

        # Selected filename label
        self.file_label = tk.Label(container, text="No file selected", fg="gray", bg="#f7b4c6")
        self.file_label.pack(pady=5)

        # Next button (disabled until file selected)
        self.next_btn = tk.Button(container, text="Next", command=self.go_next, state="disabled")
        self.next_btn.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if file_path:
            self.selected_file = file_path
            filename = file_path.split("/")[-1]  # just filename
            self.file_label.config(text=f"Selected: {filename}", fg="black")
            self.next_btn.config(state="normal")

    def go_next(self):
        if not self.selected_file:
            return

        # Save the selected file path in CreateFlyerPage's flyer_data dictionary
        self.controller.flyer_data['excel_path'] = self.selected_file

        # Call make_collage function (should be imported or defined elsewhere)
        collage_result = make_collage(self.selected_file)
        self.controller.collage = collage_result

        print("Collage created:", collage_result is not None)

        # Move to next step in CreateFlyerPage (step2)
        self.controller.show_step('step2')

        
class ChooseImagesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class PreviewEntriesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
class ConfirmEditEntryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class DonePageFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller