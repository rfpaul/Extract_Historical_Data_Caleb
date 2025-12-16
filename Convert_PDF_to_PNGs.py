#!/usr/bin/env python3
#
# Convert_PDF_to_PNGs.py
#
# This is a simple helper script to take a PDF and convert it to PNG pages using
# the pdf2image package: https://github.com/Belval/pdf2image
#
# Comments between two asterisks (**) indicate areas that should be changed to
# reflect your own data and directory structures.
#
# Please note that you may have to download or build poppler if you didn't
# install it through conda-forge.
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

from pdf2image import convert_from_path
from PIL import Image
from os import path, replace

# ** Path to the PDF you want to convert to a series of images **
pdf_path = r"C:\Your\PDF\to\convert\here.pdf"

# ** Directory to save converted images to **
dest_dir = r'C:\Your\destination\directory\here'

# ** Base filename to use for converted images **
filename_prefix = "Your output filename here-p."
# ** Start numbering the filenames here (e.g., the first page number) **
filename_numbering_start=15
# ** Number of digits for zero-padding the filename number (e.g., 42 => '042') **
filename_number_padding=3
# ** Output image format **
image_format = 'png'

print(f"Converting {pdf_path} to images...")
# ** Change DPI as needed to maintain clarity/legibility of text or other
# details; poppler_path can be excluded if you installed poppler from
# conda-forge OR have poppler in your PATH variables **
images_out = convert_from_path(pdf_path,
                               dpi=300,
                               output_folder=dest_dir,
                               fmt=image_format)#,
                               #poppler_path = r'C:\path\to\poppler-xx\bin')

print("Conversion complete. Renaming image files...")
# Rename images
for i, curr_img in enumerate(images_out, start = filename_numbering_start):
    # Close current image I/O stream
    curr_img.close()
    # Generate the new filename
    new_name = f"{filename_prefix}{str(i).zfill(filename_number_padding)}.{image_format}"
    # ...And rename the file
    replace(curr_img.filename, path.join(dest_dir, new_name))
