#!/usr/bin/env python3
#
# Convert_PDF_to_PNGs.py
#
# This is a simple helper script to take a PDF and convert it to PNG pages using
# the pdf2image package: https://github.com/Belval/pdf2image
# Please note that Windows users will have to download or build poppler for this
# script to work.
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

pdf_path = r'C:\path\to\the\PDF\you\want\to\convert.pdf'

dest_dir = r'C:\path\to\your\PNG\output\directory'

# Change DPI as needed to maintain clarity/legibility of text or other details
convert_from_path(pdf_path, dpi=300, output_folder=dest_dir, fmt='png', poppler_path = r'C:\path\to\poppler-xx\bin')
