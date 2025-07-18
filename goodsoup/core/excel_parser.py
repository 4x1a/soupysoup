# -*- coding: utf-8 -*-
"""excel_parser.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ecQtjz-7PxQWmQNAWQauZyCuHAKwLl6z
"""

# going to be excel_parser.py
import random
from pathlib import Path
import pandas as pd
from models.item import Item
from models.collage2 import Collage
from datetime import datetime
import re

def parse_excel_to_collage(excel_path: Path) -> Collage:
    df = pd.read_excel(excel_path)
    print(df.head())
    df = df.dropna(how='all')
    df.columns = [col.lower().strip() for col in df.columns]

    column_alternatives = {
        'name': ['name', 'description'],
        'chinese name': ['chinese name', 'product', 'item'],
        'price': ['price'],
        'image': ['image', 'picture']
    }

    actual_cols = {}
    for category, opts in column_alternatives.items():
        matches = [c for c in df.columns if c in opts]
        if matches:
            actual_cols[category] = matches[0]
        else:
            raise ValueError(f"Missing column for '{category}'. Options: {opts}")

    # Build a list first to maintain row order
    items_list = []
    for _, row in df.iterrows():
        if row.isna().all():
            continue
        items_list.append(
            Item(
                row[actual_cols['name']],
                row[actual_cols['chinese name']],
                row[actual_cols['price']],
                row[actual_cols['image']],
            )
        )

    # Convert it into a dict with sequential integer keys
    items_dict = {i: item for i, item in enumerate(items_list)}
    print('madde here ')

    collage_name, start_date, end_date = extract_collage_metadata_from_filename(str(excel_path))
    return Collage(name=collage_name, items_list=items_dict, start_date=start_date, end_date=end_date)
def extract_collage_metadata_from_filename(filename: str):
    """
    Parses filenames like 'weeklysale01102025-01112025.xlsx' and returns:
    - Human-readable collage name
    - start_date (datetime)
    - end_date (datetime)
    """
    match = re.search(r'(\d{8})-(\d{8})', filename)
    if not match:
        num = random.randint(1, 888)
        return "Weekly Sale"+str(num), None, None  # fallback


    start_str, end_str = match.groups()
    fmt = "%m%d%Y"


    try:
        start_date = datetime.strptime(start_str, fmt)
        end_date = datetime.strptime(end_str, fmt)

        # Format the name
        if start_date.year == end_date.year:
            if start_date.month == end_date.month:
                # Jan 10–11, 2025
                date_str = f"{start_date.strftime('%b')} {start_date.day}–{end_date.day}, {start_date.year}"
            else:
                # Jan 30 – Feb 2, 2025
                date_str = f"{start_date.strftime('%b %d')} – {end_date.strftime('%b %d')}, {start_date.year}"
        else:
            # Dec 31, 2024 – Jan 1, 2025
            date_str = f"{start_date.strftime('%b %d, %Y')} – {end_date.strftime('%b %d, %Y')}"

        name = f"Weekly Sale {date_str}"
        return name, start_date, end_date

    except ValueError:
        return "Weekly Sale", None, None