"""
This script will go through fund_data folder and move jsons with a non-empty holdings list to a differnt folder 
This is done to avoid any problems that might arise later during clustering
"""

import os
import shutil
import json

raw_folder = 'fund_data'
processed_folder = 'fund_data_processed'

valid = 0
empty = 0

for filename in os.listdir(raw_folder):
    raw_path = os.path.join(raw_folder, filename)
    processed_path = os.path.join(processed_folder, filename)

    with open(raw_path, 'r') as f:
        content = json.load(f)
        if content.get('holdings') and len(content['holdings']) > 0:
            shutil.copy2(raw_path, processed_path)
            valid += 1
        else:
            empty += 1

print(f"Total raw file count = {valid + empty}")
print(f"Valid fund count = {valid}")
print(f"Empty fund count = {empty}")