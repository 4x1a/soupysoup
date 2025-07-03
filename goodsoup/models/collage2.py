#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
class Collage
"""

import os
from app_config import BASE_DIR, ASSETS_DIR, GRAPHICS_EXCELS_DIR, FONT_PATH_BOLD, FONT_PATH_CN, FONT_PATH_EN, FILLER_PATH, PRICEBOX_PATH

from PIL import Image, ImageFont, ImageDraw
from models.item import Item
from core.image_loader import load_image
import math
from io import BytesIO
import warnings
warnings.simplefilter('always')
from core.image_utils import render_price_to_image, render_stacked_text, center_text_on_canvas, scale


COLUMNS = 3

SQ_SIZE = (2160,2160)

class Collage:
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
        box_width = self.rectw
        box_height = self.recth
    
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
        base_canvas = Image.new('RGBA',(SQ_SIZE),(255,255,255,0))
        if all(item.selected_image_path is not None for item in self.items_list.values()):
            self.rectw = int(base_canvas.width/self.items_per_row)
            self.num_rows = base_canvas.height//self.rectw
            self.recth = int(base_canvas.height/self.num_rows)
            self.items_pp = self.items_per_row*self.num_rows
            self.text_size()
            
            self.makepages()

        
    def makepages(self):
        for page_i in range(1): #math.ceil(len(self.items_list)/items_pp):
            base_canvas = Image.new('RGBA',(SQ_SIZE),(255,255,255,255))

            canvas = base_canvas.copy()
            index_of_first_item_on_page = page_i*self.items_pp
            for item_j in range(index_of_first_item_on_page,index_of_first_item_on_page+self.items_pp):
                x_coord = self.rectw * (item_j % self.items_per_row)
                y_coord = self.recth * (item_j // self.items_per_row)

                rectangle = Image.new('RGBA',(self.rectw,self.recth),(255,255,255,0))
        
                if item_j<len(self.items_list):
                    item = self.items_list[item_j]
                    img = item.foodpic()
                    img = img.resize((self.rectw,self.rectw))
                    #paste foodpic
                    rectangle.paste(img)

                    ## pricebox
                    with Image.open(PRICEBOX_PATH) as pb_img:
                        pricebox = pb_img.convert('RGBA').copy()
                        resized_pricebox = pricebox.resize(
                            (self.rectw // 2, self.recth//3),
                        resample=Image.LANCZOS
                                   ).copy()
                    base_font_scale=resized_pricebox.height/3
                    min_size = 10
                    big_size = max(int(base_font_scale*1.4),min_size)
                    super_size = max(int(base_font_scale*0.72),min_size)
                    unit_size=max(int(base_font_scale*0.5),min_size)
                    prefix_size = max(int(base_font_scale*0.72),min_size)

                    fonts = {
                        'big': ImageFont.truetype(FONT_PATH_BOLD, size=big_size),
                        'super': ImageFont.truetype(FONT_PATH_EN, size=super_size),
                        'unit': ImageFont.truetype(FONT_PATH_EN, size=unit_size),
                        'prefix': ImageFont.truetype(FONT_PATH_EN, size=prefix_size)
                    }

                    scale_factor = 4
                    large_box_size = (
                        resized_pricebox.width * scale_factor,
                        resized_pricebox.height * scale_factor
                    )
                    
                    fonts_large = {
                        k: ImageFont.truetype(f.path, size=f.size * scale_factor)
                        for k, f in fonts.items()
                    }

                    hires_price_image = render_price_to_image(
                        price_text = item.price.strip(),
                        box_size = large_box_size,
                        fonts = fonts_large
                    )

                    raw_price_image = hires_price_image.resize(
                        (resized_pricebox.width,resized_pricebox.height),
                        resample=Image.LANCZOS
                    )
                    offset_x = (resized_pricebox.width - raw_price_image.width) // 2
                    offset_y = (resized_pricebox.height - raw_price_image.height) // 2
                    resized_pricebox.paste(raw_price_image,(offset_x,offset_y), raw_price_image)

                    #paste pricebox
                    pricebox_x = rectangle.width-resized_pricebox.width-1
                    pricebox_y=rectangle.height-resized_pricebox.height
                    rectangle.paste(resized_pricebox,(pricebox_x,pricebox_y),resized_pricebox)

                    ## stacked text
                    stacked_text_img = render_stacked_text(item.chinese_name, item.name, font_size=self.max_text_size)
                    texth = min(self.recth/6,stacked_text_img.height)
                    centered_text = center_text_on_canvas(
                        stacked_text_img,
                        ### here we just set it to the (rectw,recth) because thats
                        ### what we fit the text to
                        self.rectw,
                        texth
                    )
                    rectangle.paste(centered_text, (0,centered_text.height//2),centered_text)


                else:
                    with Image.open(FILLER_PATH) as filler_img:
                        img= filler_img.convert('RGBA').resize((rectangle.width,rectangle.width))
                        rectangle.paste(img(0,0))
                print(f'look here rect size {rectangle.size} \ncanvas: {canvas.size}')
                rectangle.convert('RGB')
                canvas.paste(rectangle,(x_coord,y_coord))
            savefileas = self.name+'.png'

            white_bg = Image.new("RGB", canvas.size, (255, 255, 255))
            white_bg.paste(canvas, mask=canvas.split()[3])
            white_bg.save(os.path.join(GRAPHICS_EXCELS_DIR, savefileas))

                


            
