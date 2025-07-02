#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 17:01:11 2025

APP GOOEY I MOVED IT OUT OF STATE.py
"""
from app_config import IMG_EXTS, IMAGES_DIR
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk, Scrollbar, Listbox, StringVar, END
from core.state import AppState
from core.image_loader import load_image
from gooey.header import Header
import os
from core.no_gui_main import make_collage
from core.image_utils import find_matching_images

import warnings
warnings.simplefilter('always')

import threading
import queue
from PIL import Image, ImageTk
#from gooey.CreateFlyerPage_Subpages import SelectExcelFrame, ChooseImagesFrame, PreviewEntriesFrame, ConfirmEditEntryFrame, DonePageFrame
    
import threading
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ANNAXANNAXANNA")
        self.geometry("1000x800")
        self.configure(bg="#f7b4c6")

        self.state = None  # Initialize later

        # UI layout setup
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container  # Save for reuse

        self.frames = {}
        for F in (StartPage, ProcessImagesPage, CreateFlyerPage, UpdateImagePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        # Start loading AppState in background
        threading.Thread(target=self.load_state_in_background, daemon=True).start()

    def load_state_in_background(self):
        from app_state import AppState  # Import here if it's slow
        state = AppState(IMAGES_DIR)
        # Back on main thread, set the state
        self.after(0, lambda: self.set_app_state(state))

    def set_app_state(self, state):
        self.state = state
        print("✅ AppState loaded.")

        #Notify StartPage
        start_page = self.frames.get("StartPage")
        if hasattr(start_page, "notify_ready"):
            start_page.notify_ready()


    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]
        if hasattr(frame, 'set_data'):
            frame.set_data(**kwargs)
        frame.tkraise()
        
    def show_home(self):
        old_page = self.frames.get("CreateFlyerPage")
        if old_page:
            old_page.destroy()

        container = old_page.master
        new_page = CreateFlyerPage(parent=container, controller=self)
        new_page.grid(row=0, column=0, sticky="nsew")
        self.frames["CreateFlyerPage"] = new_page

        self.show_frame("StartPage")

from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f7b4c6")
        self.controller = controller
        
        self.header = Header(self, controller)
        self.header.pack(side="top", fill="x")

        # --- Loading spinner and label ---
        self.loading_frame = tk.Frame(self, bg="#f7b4c6")
        self.loading_label = tk.Label(self.loading_frame, text="Loading images...", font=("Helvetica", 20), bg="#f7b4c6")
        self.spinner = ttk.Progressbar(self.loading_frame, mode="indeterminate", length=200)

        self.loading_label.pack(pady=(50, 10))
        self.spinner.pack(pady=10)
        self.loading_frame.pack(expand=True)

        self.spinner.start(10)  # start spinning immediately

        # --- Content to show after loading ---
        self.ready_frame = tk.Frame(self, bg="#f7b4c6")

        self.title_label = tk.Label(self.ready_frame, text="Welcome!", font=("Helvetica", 40, "bold italic"),
                                    bg="#084b39", fg="#f7b4c6")
        self.title_label.pack(pady=20)

        self.process_btn = tk.Button(self.ready_frame, text="Process Images",
                                     command=lambda: controller.show_frame("ProcessImagesPage"))
        self.process_btn.pack(pady=10)

        self.flyer_btn = tk.Button(self.ready_frame, text="Create Graphic Flyer",
                                   command=lambda: controller.show_frame("CreateFlyerPage"))
        self.flyer_btn.pack(pady=10)

        # Keep the ready_frame hidden for now
        self.ready_frame.pack_forget()

    def notify_ready(self):
        """Called when AppState is finished loading."""
        # Stop and hide spinner
        self.spinner.stop()
        self.loading_frame.pack_forget()

        # Show main UI
        self.ready_frame.pack(expand=True)

# Assuming you have these already:
# - load_image(path, size, as_tk)
# - clear_cache()
# - Header class
# - controller.state.query_images
# - controller.show_frame

class ProcessImagesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f7b4c6")
        self.controller = controller

        self.load_generation = 0  # to track image load cycles

        # Add header at the top
        header = Header(self, controller)
        header.grid(row=0, column=0, sticky="ew")

        # Configure grid for the rest of the page content
        self.grid_rowconfigure(3, weight=1)  # scrollable results area row
        self.grid_columnconfigure(0, weight=1)

        # --- Search & filter controls ---
        search_frame = tk.Frame(self, bg="#f7b4c6")
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        search_frame.grid_columnconfigure(4, weight=1)

        tk.Label(search_frame, text="Categories:", bg="#f7b4c6").grid(row=0, column=0, sticky="w")
        self.category_listbox = tk.Listbox(search_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        self.category_listbox.grid(row=1, column=0, sticky="w")
        self.update_category_list()

        tk.Label(search_frame, text="Keyword:", bg="#f7b4c6").grid(row=0, column=1, sticky="w", padx=(10,0))
        self.keyword_entry = tk.Entry(search_frame)
        self.keyword_entry.grid(row=1, column=1, sticky="w", padx=(10,0))

        tk.Label(search_frame, text="Sort by:", bg="#f7b4c6").grid(row=0, column=2, sticky="w", padx=(10,0))
        self.sort_by_var = tk.StringVar(value='name')
        sort_options = ['name', 'category']
        ttk.OptionMenu(search_frame, self.sort_by_var, 'name', *sort_options).grid(row=1, column=2, sticky="w", padx=(10,0))

        self.reverse_var = tk.BooleanVar(value=False)
        tk.Checkbutton(search_frame, text="Descending", variable=self.reverse_var, bg="#f7b4c6").grid(row=1, column=3, sticky="w", padx=(10,0))

        tk.Button(search_frame, text="Search", command=self.run_query).grid(row=1, column=4, sticky="w", padx=(10,0))

        # --- Scrollable results area ---
        results_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        results_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(results_frame, bg="#f7b4c6")
        self.scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f7b4c6")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Pagination ---
        pagination_frame = tk.Frame(self, bg="#f7b4c6")
        pagination_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        pagination_frame.grid_columnconfigure(1, weight=1)

        self.prev_button = tk.Button(pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.grid(row=0, column=0, sticky="w")

        self.page_label = tk.Label(pagination_frame, text="Page 1", bg="#f7b4c6")
        self.page_label.grid(row=0, column=1)

        self.next_button = tk.Button(pagination_frame, text="Next", command=self.next_page)
        self.next_button.grid(row=0, column=2, sticky="e")

        # Data and pagination state
        self.current_results = []
        self.page = 0
        self.page_size = 15

        # Queue and threading setup
        self.load_queue = queue.Queue()
        self.after(100, self.process_load_queue)

        # Initial load
        self.run_query()

    def update_category_list(self):
        self.category_listbox.delete(0, tk.END)
        for cat in sorted(self.controller.state.categories):
            self.category_listbox.insert(tk.END, cat)

    def run_query(self):
        selected_indices = self.category_listbox.curselection()
        selected_categories = [self.category_listbox.get(i) for i in selected_indices]
        keyword = self.keyword_entry.get().strip()
        sort_by = self.sort_by_var.get()
        reverse = self.reverse_var.get()

        self.current_results = self.controller.state.query_images(
            categories=selected_categories if selected_categories else None,
            keyword=keyword if keyword else None,
            sort_by=sort_by,
            reverse=reverse
        )
        self.page = 0
        self.load_generation += 1  # New load cycle
        self.load_current_page()

    def load_current_page(self):
        # Clear current UI entries
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        start = self.page * self.page_size
        end = start + self.page_size
        page_items = self.current_results[start:end]

        # Put load requests in the queue
        thumbnail_size = (100, 100)
        generation = self.load_generation  # capture current generation for closure

        for img in page_items:
            self.load_queue.put((img, thumbnail_size, generation))

        total_pages = max(1, (len(self.current_results) - 1) // self.page_size + 1)
        self.page_label.config(text=f"Page {self.page + 1} of {total_pages}")

        self.prev_button.config(state="normal" if self.page > 0 else "disabled")
        self.next_button.config(state="normal" if self.page < total_pages - 1 else "disabled")

    def process_load_queue(self):
        try:
            while True:
                img, size, generation = self.load_queue.get_nowait()
                # Start a thread to load the image so UI stays responsive
                threading.Thread(target=self.load_image_thread, args=(img, size, generation), daemon=True).start()
        except queue.Empty:
            pass
        self.after(100, self.process_load_queue)  # Keep checking queue periodically

    def load_image_thread(self, img, size, generation):
        tk_img = load_image(img.file_path, size=size)
        # Return to main thread to update UI
        self.after(0, self.create_image_button, img, tk_img, generation)

    def create_image_button(self, img, tk_img, generation):
        # Only update UI if this load is still current
        if generation != self.load_generation:
            return  # Stale load, ignore

        # Find scrollable_frame is still valid (hasn't been destroyed)
        if not self.scrollable_frame.winfo_exists():
            return

        # Create the frame and button for the image
        row_frame = tk.Frame(self.scrollable_frame, bg="#f7b4c6")
        row_frame.pack(fill="x", padx=5, pady=5)

        if tk_img:
            btn = tk.Button(row_frame, image=tk_img,
                            command=lambda i=img: self.controller.show_frame('UpdateImagePage', image_metadata=i))
            btn.image = tk_img  # keep reference
            btn.pack(side="left", padx=5)
        else:
            tk.Label(row_frame, text="[Missing image]", bg="#f7b4c6").pack(side="left", padx=5)

        text = f"{img.category} / {img.name}"
        tk.Label(row_frame, text=text, font=("Helvetica", 25), anchor="w", justify="left", bg="#f7b4c6")\
            .pack(side="left", padx=10, fill="x", expand=True)

    def next_page(self):
        if (self.page + 1) * self.page_size < len(self.current_results):
            self.page += 1
            self.load_generation += 1  # Increment generation for new load
            self.load_current_page()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.load_generation += 1
            self.load_current_page()

            
""" UPDATEIMAGEPAGE"""

class UpdateImagePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f7b4c6")
        self.controller = controller

        # Header
        tk.Label(self, text="Update Image", font=("Helvetica", 40, "bold italic"),
                 bg="#084b39", fg="#f7b4c6").pack(pady=10)

        # Image display
        self.image_label = tk.Label(self, bg="#f7b4c6")
        self.image_label.pack(pady=10)

        # Frame for inputs
        form_frame = tk.Frame(self, bg="#f7b4c6")
        form_frame.pack(pady=10)

        # Filename input
        tk.Label(form_frame, text="Filename:", bg="#f7b4c6").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.filename_entry = tk.Entry(form_frame, width=40)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5)

        # Folder/category dropdown
        tk.Label(form_frame, text="Folder (category):", bg="#f7b4c6").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.folder_var = tk.StringVar()
        self.folder_menu = ttk.OptionMenu(form_frame, self.folder_var, '')
        self.folder_menu.grid(row=1, column=1, padx=5, pady=5)

        # Save button
        save_btn = tk.Button(self, text="Save", command=self.save_changes)
        save_btn.pack(pady=10)

        # Back button (optional)
        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame('ProcessImagesPage'))
        back_btn.pack(pady=5)

        # To store image metadata
        self.image_metadata = None
        self.tk_img = None  # keep reference to prevent GC

    def set_data(self, image_metadata):
        """Called by controller.show_frame to pass image metadata"""
        self.image_metadata = image_metadata

        # Prefill filename
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, image_metadata.name)

        # Update folder dropdown options
        categories = sorted(self.controller.state.categories)
        menu = self.folder_menu["menu"]
        menu.delete(0, "end")
        for cat in categories:
            menu.add_command(label=cat, command=lambda c=cat: self.folder_var.set(c))
        # Set current category
        self.folder_var.set(image_metadata.category)

        # Load and show image
        thumbnail_size = (300, 300)
        self.tk_img = load_image(image_metadata.file_path, size=thumbnail_size, as_tk=True)
        if self.tk_img:
            self.image_label.config(image=self.tk_img, text="")
        else:
            self.image_label.config(text="[Failed to load image]", image="")

    def save_changes(self):
        new_name = self.filename_entry.get().strip()
        new_category = self.folder_var.get().strip()

        if not new_name:
            messagebox.showerror("Error", "Filename cannot be empty.")
            return

        # Check for invalid characters (basic check)
        if any(c in new_name for c in r'<>:"/\|?*'):
            messagebox.showerror("Error", "Filename contains invalid characters.")
            return

        # Rename if folder/category changed
        old_path = self.image_metadata.file_path
        current_category = self.image_metadata.category

        if new_category != current_category:
            # Move to new folder
            new_dir = os.path.join(self.controller.state.root_folder, new_category)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            new_path = os.path.join(new_dir, new_name)
        else:
            # Same folder, just rename
            new_path = os.path.join(os.path.dirname(old_path), new_name)

        try:
            self.controller.state.rename_image(self.image_metadata, new_name)
            # If category changed, physically move file
            if new_category != current_category:
                os.replace(old_path, new_path)
                # Update metadata
                self.image_metadata.file_path = new_path
                self.image_metadata.category = new_category
                self.controller.state.index_images()  # refresh all data

            messagebox.showinfo("Success", "Image updated successfully!")
            # Optionally go back
            self.controller.show_frame('ProcessImagesPage')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename/move image: {e}")

class CreateFlyerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.subpages = {}
        self.collage = None
        self.current_item_index = 0

        self.init_subpages()
        self.show_subpage("get_excel")

    def init_subpages(self):
        self.subpages["get_excel"] = GetExcelPage(self, self.controller)
        self.subpages["select_image"] = SelectImagePage(self, self.controller)
        self.subpages["review"] = ReviewPage(self, self.controller)
        self.subpages["done"] = DonePage(self, self.controller)

        for page in self.subpages.values():
            page.pack(fill='both', expand=True)
            page.pack_forget()

    def show_subpage(self, name):
        for page in self.subpages.values():
            page.pack_forget()
        self.subpages[name].pack(fill='both', expand=True)

    def load_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                collage = make_collage(file_path)
                if not collage or not hasattr(collage, 'items_list') or not collage.items_list:
                    messagebox.showerror("Error", "Collage has no items.")
                    self.show_subpage("get_excel")
                    return

                self.collage = collage
                self.current_item_index = 0
                self.start_select_images()
            except ValueError:
                messagebox.showerror("Error", "Invalid data, please try again.")
                self.show_subpage("get_excel")

    def start_select_images(self):
        if self.current_item_index < len(self.collage.items_list):
            item = self.collage.items_list[self.current_item_index]

            # get full list of dicts
            state = self.controller.state
            search_results = find_matching_images(item.name, item.chinese_name, state)
    
            item.possible_images = search_results  # keep full data
    
            self.subpages["select_image"].load_item(item)
            self.show_subpage("select_image")
        else:
            self.go_to_review()


    def next_item(self):
        self.current_item_index += 1
        self.start_select_images()

    def go_to_review(self):
        self.subpages["review"].load_items(self.collage.items_list)
        self.show_subpage("review")

    def confirm_flyer(self):
        try:
            # Add your save logic here, e.g. self.collage.save()
            self.subpages["done"].set_message("File saved successfully!")
        except Exception:
            self.subpages["done"].set_message("Problem saving file.")
        self.show_subpage("done")

    def return_home(self):
        self.controller.show_home()


class GetExcelPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.master_page = parent  # parent is CreateFlyerPage

        tk.Label(self, text="Step 1: Select Excel File").pack(pady=20)
        tk.Button(self, text="Choose File", command=self.master_page.load_excel).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.controller.show_home).pack(pady=10)

class SelectImagePage(tk.Frame):
    """
    Wizard subpage to let user select an image for one item.
    Shows possible images as thumbnails in a grid (no scrollbar).
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.item = None  # current item instance

        # Title label (item name + chinese name)
        self.title_label = tk.Label(self, text="", font=('Arial', 14))
        self.title_label.pack(pady=10)

        # Frame for image buttons grid
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(padx=10, pady=10)

        # Keep references to image button widgets and their images
        self.image_buttons = []
        self.image_refs = []

        # Cancel button
        tk.Button(self, text="Cancel", command=self.controller.show_home).pack(pady=10)

    def load_item(self, item):
        self.item = item
        self.title_label.config(text=f"{item.name} / {item.chinese_name}")
    
        # Clear old buttons & images
        for btn in self.image_buttons:
            btn.destroy()
        self.image_buttons.clear()
        self.image_refs.clear()
    
        search_results = item.possible_images
    
        columns = 4
        row = 0
        col = 0
    
        for res in search_results:
            img_path = res['path']
            score = res.get('score', 0)
    
            thumb = load_image(img_path, size=(100, 100))
    
            btn = tk.Button(self.grid_frame, image=thumb,
                            command=lambda p=img_path: self.select_image(p))
            btn.image = thumb  # keep reference
            btn.grid(row=row, column=col, padx=5, pady=5)
    
            lbl = tk.Label(self.grid_frame, text=f"Score: {score}")
            lbl.grid(row=row+1, column=col, padx=5, pady=(0,10))
    
            self.image_buttons.append(btn)
            self.image_buttons.append(lbl)
            self.image_refs.append(thumb)
    
            col += 1
            if col >= columns:
                col = 0
                row += 2


    def select_image(self, img_path):
        """
        Called when user clicks on an image:
        - set selected image
        - tell CreateFlyerPage to go to next item
        """
        if self.item:
            self.item.set_selected_image(img_path)
            print(f"Selected image for {self.item.name}: {img_path}")

        flyer_page = self.controller.frames.get("CreateFlyerPage")
        if flyer_page:
            flyer_page.next_item()
        else:
            print("Error: CreateFlyerPage not found in controller.frames")



class ReviewPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.master_page = parent

        # Vertical scrollable frame
        self.scroll_canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0,0), window=self.scroll_frame, anchor='nw')
        self.scroll_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        self.scroll_canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        tk.Button(self, text="Confirm and Save", command=self.master_page.confirm_flyer).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.controller.show_home).pack(pady=5)

    def load_items(self, items):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for item in items:
            frame = tk.Frame(self.scroll_frame, pady=2)
            tk.Label(frame, text=item.name).pack(side='left', padx=5)
            tk.Label(frame, text=item.chinese_name).pack(side='left', padx=5)
            tk.Label(frame, text=item.price).pack(side='left', padx=5)
            if item.selected_image:
                thumb = load_thumbnail(item.selected_image)
                lbl = tk.Label(frame, image=thumb)
                lbl.image = thumb  # keep reference
                lbl.pack(side='left', padx=5)
            frame.pack(fill='x', pady=2)



class DonePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.master_page = parent

        self.message = tk.Label(self, text="", font=('Arial', 14))
        self.message.pack(pady=20)

        tk.Button(self, text="Return Home", command=self.controller.show_home).pack(pady=10)

    def set_message(self, text):
        self.message.config(text=text)

if __name__ == "__main__":
    app = App()
    app.mainloop()