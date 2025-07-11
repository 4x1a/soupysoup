#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#for indexing imgs
"""
import os
import re

from pypinyin import lazy_pinyin
from core.image_utils import score_filename
import tkinter as tk
from tkinter import ttk, Scrollbar, Listbox, StringVar, END
from app_config import IMG_EXTS, IMAGES_DIR
# core/state.py

class ImageMetadata:
    def __init__(self, path):
        self.file_path = path
        self.name = os.path.basename(path)
        self.category = os.path.basename(os.path.dirname(path))

        # Add created and modified timestamps (seconds since epoch)
        stat = os.stat(path)
        self.created_time = stat.st_ctime
        self.modified_time = stat.st_mtime


class AppState:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.image_list = []
        self.image_dict = {}
        self.categories = set()
        self.index_images()

    def process_images(self):
        ## check if there are images needed to be processed
        print('fix')


    def index_images(self):
        self.image_list.clear()
        self.image_dict.clear()
        self.categories.clear()

        for dirpath, _, files in os.walk(self.root_folder):
            for f in files:
                if f.lower().endswith(IMG_EXTS):
                    full_path = os.path.join(dirpath, f)
                    metadata = ImageMetadata(full_path)
                    self.image_list.append(metadata)
                    self.image_dict[full_path] = metadata
                    self.categories.add(metadata.category)
                    
    def rename_image(self, image_metadata, new_full_path):
        old_path = image_metadata.file_path
        new_full_path = os.path.abspath(new_full_path)  # Ensure absolute path
    
        new_dir = os.path.dirname(new_full_path)
        if not os.path.exists(new_dir):
            raise FileNotFoundError(f"Target folder '{new_dir}' does not exist.")
    
        if os.path.exists(new_full_path):
            raise FileExistsError("File with this name already exists.")
    
        os.rename(old_path, new_full_path)
    
        # Update metadata
        image_metadata.file_path = new_full_path
        image_metadata.name = os.path.basename(new_full_path)
        image_metadata.category = os.path.basename(new_dir)
    
        # Update dict keys
        del self.image_dict[old_path]
        self.image_dict[new_full_path] = image_metadata


    def query_images(self, categories=None, keyword=None, sort_by='name', reverse=False):
        # If categories is None or empty list, include all images (no category filter)
        if not categories:
            filtered_images = self.image_list
        else:
            category_set = set(categories)
            filtered_images = [img for img in self.image_list if img.category in category_set]
    
        keywords = []
        if keyword:
            keywords = [kw.strip() for kw in re.split(r'\s+', keyword.lower()) if kw.strip()]
            # Filter further by keyword presence (optional but speeds scoring)
            filtered_images = [img for img in filtered_images if any(kw in img.name.lower() for kw in keywords)]
    
        if keywords:
            scored = []
            for img in filtered_images:
                score, _ = score_filename(img.name, keywords)
                scored.append((score, img))
            # Sort primarily by score descending
            scored.sort(key=lambda x: x[0], reverse=True)
            result = [img for score, img in scored]
            # Reverse if requested
            if reverse:
                result.reverse()
        else:
            # Sort by given sort key if no keywords
            if sort_by == 'name':
                result = sorted(filtered_images, key=lambda img: ''.join(lazy_pinyin(img.name)).lower(), reverse=reverse)
            elif sort_by == 'created':
                result = sorted(filtered_images, key=lambda img: img.created_time, reverse=reverse)
            elif sort_by == 'modified':
                result = sorted(filtered_images, key=lambda img: img.modified_time, reverse=reverse)
            else:
                raise ValueError(f"Unknown sort key: {sort_by}")
    
        return result
    def find_image_by_filename(self, filename):
        for metadata in self.image_list:
            if os.path.basename(metadata.file_path) == filename:
                return metadata.file_path
        return None  # Not found



"""    def select_excel(self):
        excel_file = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if excel_file:
            basename = os.path.basename(excel_file)
            collage = make_collage(basename)
            if collage:
                u_choose_images(collage, self.controller.state)
                make_n_save_graphic(collage)
                messagebox.showinfo("Success", "Flyer created and saved!")
            else:
                messagebox.showerror("Error", "Failed to create flyer.")"""