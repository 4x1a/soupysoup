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
        # background for rn
        fill_color = white
        path = self.selected_image_path or os.path.join(FOLDER_PATH, FALLBACK_IMAGE)
        img = load_image(path,as_tk=False)
        width,height = img.size
        side_length = max(width,height)

        #create new square bkgrnd
        new_img = Image.new('RGBA',(side_length,side_length),color=fill_color)

        # compute top_left corner to paste og image so its centered
        left = (side_length-width)// 2
        top = (side_length-height)//2
        new_img.paste(img,(left,top))
        return new_img


