import os
import tkinter as tk
from tkinter import ttk
from core.image_loader import load_image  # Ensure this provides PIL image loading and TK conversion

class ItemSelectorFrame(ttk.Frame):
    def __init__(self, master, items, image_index):
        super().__init__(master)
        self.items = items
        self.image_index = image_index
        self.item_frames = []

        # Reset All button
        top_controls = ttk.Frame(self)
        top_controls.pack(fill='x', pady=(5, 0))
        ttk.Button(top_controls, text="Reset All Images", command=self.reset_all_images).pack(side="right", padx=5)

        # Scrollable area
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add expandable frames
        for item in self.items:
            item_frame = ExpandableItemFrame(self.scrollable_frame, item, self.image_index)
            item_frame.pack(fill="x", padx=5, pady=3)
            self.item_frames.append(item_frame)

    def reset_all_images(self):
        for frame in self.item_frames:
            frame.reset()


class ExpandableItemFrame(ttk.Frame):
    def __init__(self, master, item, image_index):
        super().__init__(master)
        self.item = item
        self.image_index = image_index
        self.expanded = False
        self.selected_button = None
        self.image_buttons = {}
        self.images_frame = None

        # Header UI
        header = ttk.Frame(self)
        header.pack(fill='x')
        ttk.Label(header, text=item.name).pack(side="left", padx=5)

        controls = ttk.Frame(header)
        controls.pack(side="right")
        ttk.Button(controls, text="Reset", command=self.reset).pack(side="left", padx=2)
        ttk.Button(controls, text="+", width=2, command=self.toggle).pack(side="left")

    def toggle(self):
        if self.expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        if not self.images_frame:
            self.images_frame = ttk.Frame(self)
            self.images_frame.pack(fill="x")

            canvas = tk.Canvas(self.images_frame, height=100)
            canvas.pack(side="top", fill="x", expand=True)
            scroll_x = ttk.Scrollbar(self.images_frame, orient="horizontal", command=canvas.xview)
            scroll_x.pack(side="bottom", fill="x")
            canvas.configure(xscrollcommand=scroll_x.set)

            inner = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=inner, anchor="nw")

            # Get candidate image paths from index
            hint = self.item.image_hint
            image_paths = self.image_index.get(hint, [])

            for img_path in image_paths:
                thumb = load_image(img_path, size=(80, 80), as_tk=True)
                if thumb is None:
                    continue

                frame = ttk.Frame(inner, borderwidth=2, relief="flat")
                frame.pack(side="left", padx=4)

                btn = ttk.Label(frame, image=thumb)
                btn.image = thumb  # prevent garbage collection
                btn.pack()
                btn.bind("<Double-Button-1>", lambda e, p=img_path, f=frame: self.select_image(p, f))

                self.image_buttons[img_path] = frame

            inner.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            self.images_frame.pack(fill="x")

        self.expanded = True

    def collapse(self):
        if self.images_frame:
            self.images_frame.pack_forget()
        self.expanded = False

    def select_image(self, path, frame):
        if self.selected_button:
            self.selected_button.config(relief="flat", borderwidth=2)

        frame.config(relief="solid", borderwidth=3)
        self.selected_button = frame
        self.item.selected_image_path = path
        print(f"[{self.item.name}] selected image: {os.path.basename(path)}")

    def reset(self):
        self.item.selected_image_path = None
        if self.selected_button:
            self.selected_button.config(relief="flat", borderwidth=2)
            self.selected_button = None
        print(f"[{self.item.name}] image reset.")
