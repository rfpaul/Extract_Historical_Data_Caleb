#!/usr/bin/env python3
#
# Combine_JSON_Records.py
#
# Helper script to combine individual JSON records into one JSON file. The
# records are combined as nested entries with their own unique, synthesized
# keys. Comments between two asterisks (**) indicate areas that should be
# changed to reflect your own data and directory structures.
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

from os import path
from glob import glob
import json

# ** Directory + search wildcard location where the individual JSONs are stored **
# IMPORTANT: Keep the wildcard "*" character for glob search!
individual_JSONs_pattern = r'C:\Your\path\to\JSON\files\*.json'

# ** Where is the fully combined JSON file going to be saved? **
json_dest = r'C:\Your\output\location\for\combined\records.json'

# ** The order of the keys in the JSON **
json_key_order = ['County', 'T', 'R', 'S', 'Mine_Index', 'Opened', 'Closed', 'Environmental_Locale', 'Mined_by', 'Owner', 'Gob_Volume', 'Problem_Area_Index', 'Problem_Acreage', 'Description']

# Get the filepaths of the JSONs
individual_JSONs_paths = glob(individual_JSONs_pattern)
individual_JSONs_paths.sort()

## Main script run

# Empty dictionary to add the entries to
combined_jsons = {}

for jpath in individual_JSONs_paths:
    with open(jpath) as j:
        try:
            # Load the current JSON
            json_entry = json.load(j)
            # ** Synthesize a unique entry index by combining these values **
            entry_index = f"{json_entry['County']}-{json_entry['Mine_Index']}"
            # Dictionary comprehension to reorder entry per the key order list
            json_entry = {key:json_entry[key] for key in json_key_order}
            # Add the JSON entry using the unique, synthesized index as a key
            combined_jsons.update({entry_index:json_entry})
        except Exception as e:
            print(f"Could not process the JSON at {jpath}")

# Save result to destination
with open(json_dest, 'w') as json_writer:
    # Pretty print the JSON with four-space indents
    json.dump(combined_jsons, json_writer, indent = '    ')
