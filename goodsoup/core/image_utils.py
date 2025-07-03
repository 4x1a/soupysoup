#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#image_utils.py in core

"""

import os
import re
from app_config import BASE_DIR, ASSETS_DIR, IMAGES_DIR, IMG_EXTS, FALLBACK_IMAGE, FONT_PATH_EN, FONT_PATH_CN
from core.useful_funcs import DPI
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.simplefilter('always')

# Make sure these are defined in your config or passed in
IMAGE_SEARCH_ROOT = IMAGES_DIR
image_extensions = IMG_EXTS
scale = int(DPI/70)
def extract_keywords(text):
    return set(re.findall(r'[\u4e00-\u9fff]+|\w+', text.lower()))


def find_matching_images(name, chinese_name, state, additional_search=None):
    keywords = extract_keywords(name + " " + chinese_name)

    if additional_search:
        keywords.update(extract_keywords(additional_search))

    results = []

    for img_meta in state.image_list:
        fname, _ = os.path.splitext(img_meta.name.lower())
        score, matched = score_filename(fname, keywords)
        if score > 0:
            results.append({
                'path': img_meta.file_path,
                'score': score,
                'matched_keywords': matched,
                'image': img_meta  # Include original metadata if needed
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    if results == []:
        results = [{'path': FALLBACK_IMAGE, 'score': 0, 'matched_keywords': ['no results found']}]
    return results

def score_filename(filename, keywords):
    """
    Score how well a filename matches a set of keywords (Chinese or English).
    Prioritizes:
    - Exact phrase matches
    - Whole-word matches
    - Substring matches
    """

    filename = filename.lower()
    score = 0
    matched_keywords = set()

    # Split filename into chunks for word-level matching
    filename_words = set(re.findall(r'[\u4e00-\u9fff]+|\w+', filename))

    for kw in keywords:
        kw = kw.lower().strip()
        if not kw:
            continue

        # If whole phrase (e.g. "corn beef") appears in filename
        if kw in filename:
            score += len(kw) * 15
            matched_keywords.add(kw)
            continue

        # If keyword is a full word in filename
        if kw in filename_words:
            score += len(kw) * 12
            matched_keywords.add(kw)
            continue

        # If keyword is a substring of any word
        partial_match_found = False
        for word in filename_words:
            if kw in word:
                score += len(kw) * 3
                matched_keywords.add(kw)
                partial_match_found = True
                break

        # Optional: slight boost if prefix of a word
        if not partial_match_found:
            for word in filename_words:
                if word.startswith(kw[:3]):
                    score += 2
                    matched_keywords.add(kw)
                    break

    return score, matched_keywords




def render_price_to_image(price_text: str, box_size: tuple[int, int], fonts: dict) -> Image.Image:
    box_w, box_h = box_size
    padding_sides = 6  # keep side padding as is

    image = Image.new("RGBA", box_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    font_big = fonts['big']
    font_super = fonts['super']
    font_unit = fonts['unit']
    font_prefix = fonts.get('prefix', font_unit)

    # Enhanced regex: prioritize multi_match first
    multi_match = re.match(r"^\s*(\d+)\s+for\s+\$?\s*(\d+(?:\.\d{1,2})?)\s*$", price_text, re.IGNORECASE)
    unit_match = None
    if not multi_match:
        unit_match = re.match(r"^\$?\s*(\d+)?(?:\.(\d{2}))?\s*(?:/|\s)?\s*(\w+)?\s*$", price_text)

    if multi_match:
        qty, price_str = multi_match.groups()
        if '.' in price_str:
            dollars, cents = price_str.split(".")
        else:
            dollars, cents = price_str, None

        prefix_text = f"{qty} for"
        dollar_text = dollars
        cents_text = f".{cents}" if cents else ""
        super_text = "$"

        prefix_bbox = draw.textbbox((0, 0), prefix_text, font=font_prefix)
        dollar_bbox = draw.textbbox((0, 0), dollar_text, font=font_big)
        cents_bbox = draw.textbbox((0, 0), ".00", font=font_super)
        super_bbox = draw.textbbox((0, 0), super_text, font=font_super)

        prefix_w = prefix_bbox[2] - prefix_bbox[0]
        prefix_h = prefix_bbox[3] - prefix_bbox[1]
        dollar_w = dollar_bbox[2] - dollar_bbox[0]
        dollar_h = dollar_bbox[3] - dollar_bbox[1]
        cents_w = cents_bbox[2] - cents_bbox[0]
        cents_h = cents_bbox[3] - cents_bbox[1]
        super_w = super_bbox[2] - super_bbox[0]
        super_h = super_bbox[3] - super_bbox[1]

        vertical_spacing = 4
        content_height = prefix_h + vertical_spacing + max(dollar_h, super_h)

        y_offset = (box_h - content_height) // 2
        y_prefix = y_offset
        y_price = y_prefix + prefix_h + vertical_spacing

        x_prefix = (box_w - prefix_w) // 2
        draw.text((x_prefix, y_prefix), prefix_text, font=font_prefix, fill=(0, 0, 0, 255))

        total_price_width = super_w + dollar_w + (cents_w if cents else 0)
        x_price = (box_w - total_price_width) // 2
        x_super = x_price
        x_dollar = x_super + super_w
        x_cents = x_dollar + dollar_w

        y_super = y_price + (dollar_h - super_h)
        draw.text((x_super, y_super), super_text, font=font_super, fill=(0, 0, 0, 255))
        draw.text((x_dollar, y_price), dollar_text, font=font_big, fill=(0, 0, 0, 255))
        if cents:
            draw.text((x_cents, y_price), cents_text, font=font_super, fill=(0, 0, 0, 255))

    elif unit_match:
        dollars, cents, unit = unit_match.groups()
        dollars = dollars or "0"
        unit = unit or ""
        has_cents = cents is not None
        cents_text = f".{cents}" if has_cents else ""
        dummy_cents = ".00"

        big_text = dollars
        dollar_sign = "$"
        sub_text = f"/{unit}" if unit else ""

        big_bbox = draw.textbbox((0, 0), big_text, font=font_big)
        dollar_bbox = draw.textbbox((0, 0), dollar_sign, font=font_super)
        real_cents_bbox = draw.textbbox((0, 0), cents_text, font=font_super)
        dummy_cents_bbox = draw.textbbox((0, 0), dummy_cents, font=font_super)
        sub_bbox = draw.textbbox((0, 0), sub_text, font=font_unit)

        big_w = big_bbox[2] - big_bbox[0]
        big_h = big_bbox[3] - big_bbox[1]
        dollar_w = dollar_bbox[2] - dollar_bbox[0]
        dollar_h = dollar_bbox[3] - dollar_bbox[1]
        cents_w = dummy_cents_bbox[2] - dummy_cents_bbox[0]
        cents_h = dummy_cents_bbox[3] - dummy_cents_bbox[1]
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_h = sub_bbox[3] - sub_bbox[1]

        total_price_width = dollar_w + big_w + cents_w
        x_start = (box_w - total_price_width) // 2

        x_dollar = x_start
        x_big = x_dollar + dollar_w
        x_cents = x_big + big_w

        top_row_height = max(big_h, dollar_h, cents_h)
        bottom_row_height = sub_h if sub_text else 0
        vertical_spacing = 4

        content_height = top_row_height + (vertical_spacing if bottom_row_height else 0) + bottom_row_height
        y_offset = (box_h - content_height) // 2

        y_top = y_offset
        y_sub = y_top + top_row_height + vertical_spacing

        draw.text((x_dollar, y_top), dollar_sign, font=font_super, fill=(0, 0, 0, 255))
        draw.text((x_big, y_top), big_text, font=font_big, fill=(0, 0, 0, 255))
        if has_cents:
            draw.text((x_cents, y_top), cents_text, font=font_super, fill=(0, 0, 0, 255))

        if sub_text:
            x_sub = x_cents + cents_w - sub_w
            x_sub = min(x_sub, box_w - sub_w - padding_sides)
            x_sub = max(x_sub, padding_sides)
            draw.text((x_sub, y_sub), sub_text, font=font_unit, fill=(0, 0, 0, 255))

    else:
        fallback_bbox = draw.textbbox((0, 0), price_text, font=font_unit)
        fallback_w = fallback_bbox[2] - fallback_bbox[0]
        fallback_h = fallback_bbox[3] - fallback_bbox[1]
        x = (box_w - fallback_w) // 2
        y = (box_h - fallback_h) // 2
        draw.text((x, y), price_text, font=font_unit, fill=(0, 0, 0, 255))

    return image

def render_stacked_text(chinese_text, english_text, font_size):
    # Scale fonts up
    font_cn = ImageFont.truetype(FONT_PATH_CN, font_size * scale)
    font_en = ImageFont.truetype(FONT_PATH_EN, font_size * scale-scale)

    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    bbox_cn = draw.textbbox((0, 0), chinese_text, font=font_cn)
    bbox_en = draw.textbbox((0, 0), english_text, font=font_en)

    w_cn = bbox_cn[2] - bbox_cn[0]
    h_cn = bbox_cn[3] - bbox_cn[1]
    w_en = bbox_en[2] - bbox_en[0]
    h_en = bbox_en[3] - bbox_en[1]

    total_width = max(w_cn, w_en)
    total_height = h_cn + h_en

    # Create hi-res canvas
    img = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate centered positions
    x_cn = (total_width - w_cn) // 2 - bbox_cn[0]
    y_cn = -bbox_cn[1]

    x_en = (total_width - w_en) // 2 - bbox_en[0]
    y_en = h_cn - bbox_en[1]

    # Draw text
    draw.text((x_cn, y_cn), chinese_text, font=font_cn, fill=(0, 0, 0, 255))
    draw.text((x_en, y_en), english_text, font=font_en, fill=(0, 0, 0, 255))

    # Downscale for smoothness
    final_img = img.resize(
        (total_width // scale, total_height // scale),
        resample=Image.LANCZOS
    )
    return final_img


def center_text_on_canvas(text_img, width, height):
    # Create transparent canvas
    canvas = Image.new("RGBA", (width, height), (255, 253, 240, 160))

    # Get position to paste (centered)
    x = (width - text_img.width) // 2
    y = (height - text_img.height) // 2

    # Paste text image with alpha
    canvas.paste(text_img, (x, y), text_img)

    return canvas
