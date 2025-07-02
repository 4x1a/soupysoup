
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
class Collage
"""

#images in assets folder 
import os
from app_config import BASE_DIR, ASSETS_DIR, HEADER_PATH, BHEADER_PATH, FONT_PATH_CN, FONT_PATH_EN, FONT_PATH_BOLD,FILLER_PATH, PRICEBOX_PATH
from PIL import Image, ImageFont, ImageDraw
from models.item import Item
from core.image_loader import load_image
from core.useful_funcs import mmtopix, pixtomm
from core.image_utils import render_price_to_image, render_stacked_text, center_text_on_canvas, scale
from fpdf import FPDF, Align
import math
from io import BytesIO
import warnings
warnings.simplefilter('always')

COLUMNS_NO=2

A4_SIZE_MM = (210, 297)          # A4: 210mm x 297mm
LEGAL_SIZE_MM = (215.9, 355.6)   # Legal: 8.5" x 14" converted to mm
TABLOID_SIZE_MM = (279.4, 431.8) # Tabloid: 11" x 17" converted to mm
LONGASS_SIZE = (150,700)

pdfsize = LONGASS_SIZE
class Collage:
    def __init__(self,name,items_list,start_date=None,end_date=None):
        self.name= name
        self.items_list=items_list
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

            
    def headers(self):
        if self.graphic is not None:
            pdfw, pdfh = self.graphic.epw, self.graphic.eph
    
            # --- Top Header ---
            if os.path.isfile(HEADER_PATH):
                with Image.open(HEADER_PATH) as header_img:
                    top = header_img.convert('RGBA').copy()
    
                w, h = top.size
                self.header_ratio = h / w
                header_h = pdfw * self.header_ratio
    
                if header_h <= pdfh / 2:
                    self.top = top
                    self.header_h = header_h
                    print(f'header height = {self.header_h}')
                else:
                    print(f'header too tall: {header_h}px > half of page height ({pdfh / 2}px)')
    
            # --- Bottom Header ---
            if os.path.isfile(BHEADER_PATH):
                with Image.open(BHEADER_PATH) as bheader_img:
                    bottom = bheader_img.convert('RGBA').copy()
    
                w, h = bottom.size
                self.bheader_ratio = h / w
                bheader_h = pdfw * self.bheader_ratio
    
                if bheader_h <= pdfh / 2:
                    self.bottom = bottom
                    self.bheader_h = bheader_h
                    print(f'bottom header height = {self.bheader_h}')
                else:
                    print(f'bottom header too tall: {bheader_h}px > half of page height ({pdfh / 2}px)')


      
        
        
        # header = os.path.join(ASSETS_DIR,'headerpic.png')
        # image1 = Image.open(header)
        # bottomheader = os.path.join(ASSETS_DIR,'bottomlogo.png')
        # image2 = Image.open(bottomheader)
        # top_header = image1.resize((2168,760),resample=Image.LANCZOS)
        # bottom_header = image2.resize((800,200),resample=Image.LANCZOS)

        # self.header = top_header # file path goes here
        # self.bottom = bottom_header #file path goes here
        # self.collage_pgs = None # how many pgs will it need
        
    def generate_pdf(self):
        # check there is a selected image for each item 
        #if {
               # }
        pdf = FPDF(unit='mm',format=pdfsize)
        pdf.set_margin(0)
        self.graphic=pdf

        self.headers()
        
        #calculate collage area
        collage_spaceh = pdf.eph-(self.header_h+self.bheader_h)
        self.collage_space = (pdf.epw,collage_spaceh)
        self.collage_cols = COLUMNS_NO #how many items per column
        self.rectw = pdf.epw/self.collage_cols
        self.max_rows = math.floor(collage_spaceh/self.rectw)
        self.recth = collage_spaceh/self.max_rows
        print(f'RECTW {self.rectw}, RECTH {self.recth}')
        
        #items pp
        print(f'look here \n max rows = {self.max_rows} and collage_cols={self.collage_cols}')
        self.items_pp = self.collage_cols*self.max_rows
        self.pages = math.ceil(len(self.items_list)/self.items_pp)
        print(f'\n\n look here self pages = {self.pages} and self.items_pp={self.items_pp}') 
        self.text_size()
        
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
            
    def makepages(self):
        pdf = self.graphic
        print('hi im at makepages')
        items = self.items_list
        header = self.top
        bottomheader = self.bottom
        bheadh_mm = self.bheader_h
        print(self.pages)
    
        for i in range(self.pages):
            print(f'i={i},itemspp={self.items_pp}')
            pdf.add_page()
            pdf.image(header, x=0, y=0, w=pdf.epw)
            pdf.image(bottomheader, x=0, y=pdf.eph - bheadh_mm, w=pdf.epw)
    
            for j in range(i * self.items_pp, (i + 1) * self.items_pp):
                local_index = j % self.items_pp
                xcol = (local_index % self.collage_cols) * self.rectw
                yrow = (local_index // self.collage_cols) * self.recth + self.header_h
    
                frame = Image.new('RGBA', (mmtopix(self.rectw), mmtopix(self.recth)), (250, 20, 140, 100))
    
                if j < len(items):
                    item = items[j]
                    img = item.foodpic().convert("RGBA")
                    img = img.resize((mmtopix(self.rectw), mmtopix(self.rectw)))
                    frame.paste(img, (0, 0))
    
                    # --- PRICE BOX ---
                    with Image.open(PRICEBOX_PATH) as pb_img:
                        pricebox = pb_img.convert('RGBA').copy()
    
                    resized_pricebox = pricebox.resize(
                        (int(mmtopix(self.rectw) / 2), int(mmtopix(self.recth) / 3)),
                        resample=Image.LANCZOS
                    ).copy()
    
                    base_font_scale = resized_pricebox.height / 3
                    min_size = 10
                    big_size = max(int(base_font_scale * 1.2), min_size)
                    super_size = max(int(base_font_scale * 0.72), min_size)
                    unit_size = max(int(base_font_scale * 0.5), min_size)
                    prefix_size = max(int(base_font_scale * 0.72), min_size)
    
                    fonts = {
                        'big': ImageFont.truetype(FONT_PATH_BOLD, size=big_size),
                        'super': ImageFont.truetype(FONT_PATH_EN, size=super_size),
                        'unit': ImageFont.truetype(FONT_PATH_EN, size=unit_size),
                        'prefix': ImageFont.truetype(FONT_PATH_EN, size=prefix_size),
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
                        price_text=item.price.strip(),
                        box_size=large_box_size,
                        fonts=fonts_large
                    )
    
                    raw_price_image = hires_price_image.resize(
                        (int(resized_pricebox.width * 0.8), int(resized_pricebox.height * 0.8)),
                        resample=Image.LANCZOS
                    )
                    offset_x = (resized_pricebox.width - raw_price_image.width) // 2
                    offset_y = (resized_pricebox.height - raw_price_image.height) // 2
                    resized_pricebox.paste(raw_price_image, (offset_x, offset_y), raw_price_image)
    
                    # Paste pricebox first
                    pricebox_x = frame.width - resized_pricebox.width - 1
                    pricebox_y = frame.height - resized_pricebox.height
                    frame.paste(resized_pricebox, (pricebox_x, pricebox_y), resized_pricebox)
    
                    # --- STACKED TEXT ---
                    stacked_text_img = render_stacked_text(item.chinese_name, item.name, font_size=self.max_text_size)
                    centered_text = center_text_on_canvas(
                        stacked_text_img,
                        int(mmtopix(self.rectw) / 2),
                        int(mmtopix(self.rectw) / 3)
                    )
                    text_y = frame.height - centered_text.height
                    text_y = max(0, text_y)  # avoid negative placement
                    frame.paste(centered_text, (0, text_y), centered_text)
    
                else:
                    with Image.open(FILLER_PATH) as filler_img:
                        img = filler_img.convert('RGBA').resize((frame.width, frame.width))
                        frame.paste(img, (0, 0))
    
                buffer = BytesIO()
                frame.convert("RGB").save(buffer, format="PNG")
                buffer.seek(0)
                pdf.image(buffer, w=self.rectw, h=self.recth, x=xcol, y=yrow)


        
        
        


    def __str__(self):
        return f'new collage instance made: {self.name}, start { self.start}, end {self.end}'
