"""
This script will check whether the stocks under the holdings list are uniformly named
We don't want one fund saying Reliance Industries Limited and other fund saying Reliance Industries Ltd. 
"""

import os
import json
import pandas as pd

processed_folder = 'fund_data_processed'
stocks = {}

for filename in os.listdir(processed_folder):
    with open(os.path.join(processed_folder, filename), 'r') as f:
        data = json.load(f)
        for holding in data.get('holdings', []):
            name = holding['name'].strip()
            stocks[name] = stocks.get(name, 0) + 1    # increment count for that particular stock

adf = pd.DataFrame(list(stocks.items()), columns = ['Name', 'Frequency'])
adf = adf.sort_values(by='Name')

adf.to_csv("./data/stock_names_audit.csv", index=False)
print(f"Total unique raw names = {len(adf)}")
``