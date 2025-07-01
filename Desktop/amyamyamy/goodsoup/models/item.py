#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 00:44:10 2025

#weekly sale
"""
from app_config import IMAGES_DIR, ASSETS_DIR, IMG_EXTS, FALLBACK_IMAGE
import os
from core.image_utils import find_matching_images  # your utility function
from PIL import Image

import warnings
warnings.simplefilter('always')
FOLDER_PATH = IMAGES_DIR  # used for quick validation

import os

class Item:
    def __init__(self, name, chinese_name, price, image_hint):
        self.name = name
        self.chinese_name = str(chinese_name)
        self.price = str(price)
        self.image_hint = str(image_hint)  # Formerly imagepath
        self.selected_image_path = None
        self.possible_images = []

    def __repr__(self):
        return f'item: {self.name} at {self.price}'
    
    def select_image(self, state):
        if self.image_hint.lower() == "blank":
            return [{'path': FALLBACK_IMAGE, 'score': 100, 'matched_keywords': ['blank']}]
    
        elif not self.image_hint:
            return find_matching_images(self.name, self.chinese_name, state)
    
        elif self.image_hint.lower().endswith(IMG_EXTS):
            full_path = os.path.join(FOLDER_PATH, self.image_hint)
            if os.path.exists(full_path):
                return [{'path': full_path, 'score': 100, 'matched_keywords': ['direct match']}]
            else:
                return find_matching_images(self.name, self.chinese_name, state)
    
        else:
            return find_matching_images(self.name, self.chinese_name, state, additional_search=self.image_hint)




    def set_selected_image(self, path):
        """
        Assigns selected_image_path safely.
        Falls back to blank if path is invalid or None.
        """
        if path and os.path.isfile(path):
            self.selected_image_path = path
            print(f"✅ Image set: {path}")
        else:
            fallback = os.path.join(ASSETS_DIR, FALLBACK_IMAGE)
            self.selected_image_path = fallback
            print(f"⚠️ Invalid path. Using fallback: {fallback}")

    def foodpic(self):
        """
        Return a PIL image (500x500 transparent square),
        centered and resized.
        """
        path = self.selected_image_path or os.path.join(FOLDER_PATH, FALLBACK_IMAGE)

        try:
            base_img = Image.open(path)
        except IOError:
            print("⚠️ Failed to open image. Using fallback.")
            base_img = Image.open(os.path.join(FOLDER_PATH, FALLBACK_IMAGE))

        square_w = 1000
        canvas = Image.new('RGBA', (square_w, square_w), (255, 255, 255, 255))

        w, h = base_img.size
        ratio = min(square_w / w, square_w / h)
        new_size = (int(w * ratio), int(h * ratio))
        resized = base_img.resize(new_size, resample=Image.BILINEAR)

        paste_x = (square_w - new_size[0]) // 2
        paste_y = (square_w - new_size[1]) // 2
        canvas.paste(resized, (paste_x, paste_y), resized if resized.mode == 'RGBA' else None)

        return canvas


