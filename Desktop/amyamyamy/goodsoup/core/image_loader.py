#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#weekly sale
#core/image_loader
"""

from PIL import Image, ImageTk
import os

# Two caches:
_thumbnail_cache = {}  # Key: (abs_path, size)
_fullsize_cache = {}   # Key: abs_path

def load_image(path: str, size: tuple[int, int] = None, as_tk: bool = True):
    """
    Loads an image from disk. Resizes and converts to ImageTk if needed.

    Args:
        path (str): Path to image.
        size (tuple[int, int], optional): Resize image to this size (width, height).
        as_tk (bool): If True, return ImageTk.PhotoImage. Otherwise, return PIL.Image.

    Returns:
        ImageTk.PhotoImage or PIL.Image or None if failed.
    """
    abs_path = os.path.abspath(path)

    if size:
        key = (abs_path, size)
        if key in _thumbnail_cache:
            return _thumbnail_cache[key]
    else:
        if abs_path in _fullsize_cache:
            return _fullsize_cache[abs_path]

    try:
        with Image.open(abs_path) as img:
            img = img.convert("RGBA")
            if size:
                img = img.resize(size, Image.LANCZOS)
            if as_tk:
                img_tk = ImageTk.PhotoImage(img)
                if size:
                    _thumbnail_cache[key] = img_tk
                return img_tk
            else:
                # Return copy to keep it usable after `with`
                img_copy = img.copy()
                if not size:
                    _fullsize_cache[abs_path] = img_copy
                return img_copy

    except Exception as e:
        print(f"[ImageLoader] ❌ Failed to load image '{path}': {e}")
        return None

def clear_cache():
    _thumbnail_cache.clear()
    _fullsize_cache.clear()
