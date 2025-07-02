#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
launcher aka entry point
#weekly sale
"""

import os
import sys
import subprocess
from app_config import BASE_DIR, IMAGES_DIR
print("Python executable:", sys.executable)
print("Python version:", sys.version)

def main():
    # Get the project root directory (parent of this launcher script)
    project_root = BASE_DIR
    
    # Run the gooey.main_window module using python -m
    #subprocess.run([sys.executable, "-m", "gooey.main_window"], cwd=project_root)
    
    subprocess.run([sys.executable, "-m", "core.no_gui_main"], cwd=project_root)

if __name__ == "__main__":
    main()