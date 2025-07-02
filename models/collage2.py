#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
class Collage
"""

import os
from app_config import {
    BASE_DIR, ASSETS_DIR, FONT_PATH_BOLD, FONT_PATH_CN, FONT_PATH_EN, FILLER_PATH, PRICEBOX_PATH
}
from PIL import Image, ImageFont, ImageDraw
from models.item import Item
from core.image_loader import load_image
import math

COLUMNS = 3

SQ_SIZE = (2160,2160)

class Collage2:
    def __init__(self,name,items_list,start_date=None,end_date=None):
        self.name = name
        self.items_list = items_list
        self.start = start_date
        self.end = end_date
        self.graphic = None

    def find_longest_names(self):
        longest_name = ''
        longest_chinese_name = ''
    
        for item in self.items_list.values():
            print(item)
            if len(item.name) > len(longest_name):
                longest_name = item.name
            if len(item.chinese_name) > len(longest_chinese_name):
                longest_chinese_name = item.chinese_name
        self.longest,self.longest_c = longest_name, longest_chinese_name

    #call text_size
    def text_size(self):
        # Get longest names
        self.find_longest_names()
        longest_en = self.longest
        longest_cn = self.longest_c
        #print(f'here i am and the longest_en word is: {longest_en}, {longest_cn}')
        #print(f'aqui is the rect wxh: {self.rectw} {self.recth}')
        ### HERE WE'RE SETTING HOW LARGE THE TEXT FOR THE NAMES' OF ITEMS WILL BE
        box_width = int(mmtopix(self.rectw))
        box_height = int(mmtopix(self.recth))
    
        max_font_size = 100  # Try from large to small
    
        for size in range(max_font_size, 5, -1):
            font_cn = ImageFont.truetype(FONT_PATH_CN, size)
            font_en = ImageFont.truetype(FONT_PATH_EN, size)
    
            img = Image.new("RGB", (box_width, box_height), "white")
            draw = ImageDraw.Draw(img)
    
            # Use textbbox to get dimensions
            bbox_cn = draw.textbbox((0, 0), longest_cn, font=font_cn)
            w_cn = bbox_cn[2] - bbox_cn[0]
            h_cn = bbox_cn[3] - bbox_cn[1]
    
            bbox_en = draw.textbbox((0, 0), longest_en, font=font_en)
            w_en = bbox_en[2] - bbox_en[0]
            h_en = bbox_en[3] - bbox_en[1]
    
            total_height = h_cn + h_en
            max_width = max(w_cn, w_en)
            #print(f'total_height= {total_height}, total_width = {max_width}')
            #print(f'lets see if max font size for loop runs {size}')
            if total_height <= box_height and max_width <= box_width:
                set2= size  # Save the first fitting font size
                break  # Done! We found the largest one that fits
        else:
            set2= 10  # Fallback if none fit
        self.max_text_size = set2
        print(f"✅ Max font size that fits: {self.max_text_size}")


        
    #call text_size
    def text_size(self):
        # Get longest names
        self.find_longest_names()
        longest_en = self.longest
        longest_cn = self.longest_c
        #print(f'here i am and the longest_en word is: {longest_en}, {longest_cn}')
        #print(f'aqui is the rect wxh: {self.rectw} {self.recth}')
        ### HERE WE'RE SETTING HOW LARGE THE TEXT FOR THE NAMES' OF ITEMS WILL BE
        box_width = int(mmtopix(self.rectw))
        box_height = int(mmtopix(self.recth))
    
        max_font_size = 100  # Try from large to small
    
        for size in range(max_font_size, 5, -1):
            font_cn = ImageFont.truetype(FONT_PATH_CN, size)
            font_en = ImageFont.truetype(FONT_PATH_EN, size)
    
            img = Image.new("RGB", (box_width, box_height), "white")
            draw = ImageDraw.Draw(img)
    
            # Use textbbox to get dimensions
            bbox_cn = draw.textbbox((0, 0), longest_cn, font=font_cn)
            w_cn = bbox_cn[2] - bbox_cn[0]
            h_cn = bbox_cn[3] - bbox_cn[1]
    
            bbox_en = draw.textbbox((0, 0), longest_en, font=font_en)
            w_en = bbox_en[2] - bbox_en[0]
            h_en = bbox_en[3] - bbox_en[1]
    
            total_height = h_cn + h_en
            max_width = max(w_cn, w_en)
            #print(f'total_height= {total_height}, total_width = {max_width}')
            #print(f'lets see if max font size for loop runs {size}')
            if total_height <= box_height and max_width <= box_width:
                set2= size  # Save the first fitting font size
                break  # Done! We found the largest one that fits
        else:
            set2= 10  # Fallback if none fit
        self.max_text_size = set2
        print(f"✅ Max font size that fits: {self.max_text_size}")

    def generate_graphics(self):
        self.items_per_row = COLUMNS
        if all(item.selected_image is not None for item in self.items_list.values()):
            self.rectw = int(canvas.width/self.items_per_row)
            self.num_rows = math.floor(canvas.height/self.rectw)
            self.recth = int(canvas.height/self.num_rows)
            self.items_pp = self.items_per_row*self.num_rows
            self.text_size()

        
    def makepages(self):
        base_canvas = Image.new('RGBA',(SQ_SIZE),(255,255,255,0))
        for page_i in math.ceil(len(self.items_list)/items_pp):
            canvas = base_canvas.copy()
            index_of_first_item_on_page = page_i*self.items_pp
            for item_j in range(index_of_first_item_on_page,index_of_first_item_on_page+self.items_pp):
                x_coord = self.rectw * (item_j % self.items_per_row)
                y_coord = self.recth * (item_j // self.items_per_row)
                item = self.items_list[item_j]
                rect = self.make_rectangle(item)
                ####

    def make_rectangle(self,item):
        rectangle = Image.new('RGBA',(self.rectw,self.recth),(255,255,255,0))
        rectangle.past()


            
