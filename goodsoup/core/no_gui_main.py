#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fake main aka no gui testing
"""
import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from gooey.header import Header
from pathlib import Path
from app_config import BASE_DIR, ASSETS_DIR, GRAPHICS_EXCELS_DIR, IMAGES_DIR
from core.excel_parser import parse_excel_to_collage
from gooey.image_selector_frame import ItemSelectorFrame
from typing import Optional
from tkinter import filedialog
import threading
from core.state import AppState
#import fpdf

def main():
    
    print('hello world')
    
    #initialize app state
    state = AppState(IMAGES_DIR)
    
    excel = 'weeklysale10-01-25to11-05-25.xlsx'
    collage = make_collage(excel)
    #make sure object instance was created
    if collage != None:
        u_choose_images(collage, state)
    
        
    make_n_save_graphic(collage)
        
    
    


#turn excel into collage

def make_collage(excelfile):
#excelfile = str(input('excel filename'))
    excelpath = Path(os.path.join(GRAPHICS_EXCELS_DIR,excelfile))
    if excelpath.is_file():
        try: 
            collage = parse_excel_to_collage(excelpath)
            return collage
        except IOError:
            print("couldn't open excel")
            return None
        
def u_choose_images(collage_inst,state):
    for item in collage_inst.items_list.values():
        #invoke the item method to generate possible images attribute
        item.possible_images = item.select_image(state)
        item.set_selected_image(item.possible_images[0]['path'])
        print(f"CHOOSING AN IMAGE{item.selected_image_path}")
        
def make_n_save_graphic(collage):
    collage.generate_graphics()
    collage.makepages()
    #print('plzzz so closeS')
    #grafic = collage.graphic
    #save_as = collage.name+'.pdf'
    #grafic.output(os.path.join(GRAPHICS_EXCELS_DIR,save_as))

if __name__ == "__main__":
    main()

    
    