#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#image index
"""

import os

def build_image_index(images_dir):
    image_index = {}
    for dirpath, _, filenames in os.walk(images_dir):
        for f in filenames:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                full_path = os.path.join(dirpath, f)
                image_index[f] = full_path  # key by filename (or tweak)
    return image_index