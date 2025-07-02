#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gooey main window:D
"""

# gui/main_window.py

import tkinter as tk
# import os
from tkinter import ttk
from tkinter import messagebox
# from gooey.header import Header
# from pathlib import Path
from app_config import BASE_DIR, ASSETS_DIR, GRAPHICS_EXCELS_DIR, IMAGES_DIR
# from core.excel_parser import parse_excel_to_collage
# from gooey.image_selector_frame import ItemSelectorFrame
# from typing import Optional
#from tkinter import filedialog
# import threading
from gooey.appclass import App
# from core.image_utils import build_image_index

def main():
    app = App()
    app.mainloop()
    
if __name__ == "__main__":
    main()