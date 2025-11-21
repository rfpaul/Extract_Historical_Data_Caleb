#!/usr/bin/env python3
#
# Batch_Crop_Images.py
#
# This helper script pre-processes images for vision language model extraction
# by aiding in the removal of extraneous content that can result in slower
# inference or inaccurate data extraction. Comments between two asterisks (**)
# indicate areas that should be changed to reflect your own data and directory
# structures.
#
# IMPORTANT: The cropping bounding box images *MUST* be PNGs including an alpha
# (transparency) channel, with the only non-transparent pixels being the one
# bounding box per image.
#
# - To create the bounding box images, add all the pages that need to be cropped
# as layers in an image editing program (e.g., Photoshop, GIMP), aligning the
# images to be cropped at the top left corner (that corner is the 0,0 coordinate
# for image files).
# - Change the blending mode for all layers as "Darken" for dark text on light
# backgrounds or "Lighten" for light text on dark backgrounds. This will make
# the bounding box area(s) apparent.
# - Create a new transparent layer for each bounding box needed.
# - Select one of the transparent layers you just created and, using the
# rectangular selection tool, draw a rectangular selection around the bounding
# box area.
# - From the Edit menu, draw a stroke (outline) along the selection.
# - For each cropping bounding box, hide all the other layers and export to RGBA
# PNG (RGB + the alpha/transparency channel).
#
# Copyright (C) 2025 The Board of Trustees of the University of Illinois
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Created/maintained by Robert Paul

## Import and setup

from os import path
from PIL import Image
from glob import glob

# ** Directory + search wildcard location of the images to crop **
# IMPORTANT: Keep the wildcard "*" character for glob search!
src_dir = r'C:\Your\images\to\crop\here\*.png'

# ** Directory to save cropped images to **
dest_dir = r'C:\Your\destination\directory\here'

# ** List with path(s) for cropping bounding box PNG(s) **
cropping_bbox_paths = [
    r'C:\Your\bounding\box\image\here\001.png',
    r'C:\Your\bounding\box\image\here\002.png'
]

# ** Numbering prefix to use in filenames if each image has multiple cropping bounding boxes (e.g., a page layout with 2 or more entries per page) **
multi_crop_prefix = '-entry.'
# ** Suffix to use in filenames to indicate that they were cropped **
cropped_suffix = "_cropped"

# Get list of filepaths for images to crop
src_paths = glob(src_dir)
src_paths.sort()

# List comprehension to load the bounding box coordinates for cropping
cropping_bboxes = [Image.open(img).getbbox() for img in cropping_bbox_paths]

## Main script run

for count, src_path in enumerate(src_paths, start=1):
    for i, bbox in enumerate(cropping_bboxes, start=1):
        # Use basename of source image to construct output filename
        base_filename = path.basename(path.splitext(src_path)[0]
        # Construct the output filename...
        if len(cropping_bboxes) > 1:
            dest_filename = f"{base_filename}{multi_crop_prefix}{i}{cropped_suffix}.png"
        else:
            dest_filename = f"{base_filename}{cropped_suffix}.png"
        # Now put it all together...
        dest_path = path.join(dest_dir, dest_filename)

        with Image.open(src_path) as src_img:
            # Crop image
            cropped_img = src_img.crop(bbox)
            # Save output
            cropped_img.save(dest_path)
    # Give progress for every 50 completed pages
    if count % 50 == 0:
        print(f"Completed cropping on image {count} of {len(src_paths)}")

print(f"Cropping completed for {len(src_paths)} images")
