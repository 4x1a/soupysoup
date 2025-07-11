#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## # NOTE TO SELF NEED TO MAKE IT SO U CAN ALSO GENERATE 
#.    A COLLAGE OBJ WITH FOLDER
## THEN U ADD ITEMS MANUALLY OR BY HAND
## WHEN U CONFIRM IT MOVES ALL THE IMAGES BACK TO MAIN FOLDER
from PIL import Image
PRICEBOX_PATH = 'yellowredspike.png'

def crop_non_transparent(image_path, output_path):
    """
    Crops the non-transparent part of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the cropped image.
    """
    try:
        img = Image.open(image_path)

        # Get the bounding box of the non-transparent region
        bbox = img.getbbox()

        if bbox:
            # Crop the image to the bounding box
            cropped_img = img.crop(bbox)
            cropped_img.save(output_path)
            print(f"Image successfully cropped and saved to {output_path}")
        else:
            print("No non-transparent pixels found in the image.")

    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_image = PRICEBOX_PATH  # Replace with your image file
output_image = PRICEBOX_PATH
crop_non_transparent(input_image, output_image)