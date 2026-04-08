import requests
import pandas as pd
import os
import json
import time
import random

# ---------- prepare the isin list for scraping ---------- #
os.makedirs('fund_data', exist_ok=True)

df = pd.read_csv('./data/cleaned_scheme_info.csv')
target_categories = [
    'Equity Scheme - Large Cap Fund',
    'Equity Scheme - Mid Cap Fund',
    'Equity Scheme - Small Cap Fund',
    'Equity Scheme - Flexi Cap Fund',
    'Equity Scheme - Multi Cap Fund',
    'Equity Scheme - Large & Mid Cap Fund',
    'Equity Scheme - Sectoral/ Thematic',
    'Equity Scheme - ELSS'
]

# keep the equity schemes in a separate dataframe
equity_df = df[df['Scheme Category'].isin(target_categories)].copy()

# this holds { isin : scheme_name } pairs
target_funds = equity_df[['ISIN', 'Scheme NAV Name']].to_dict('records')

print(f"ISIN list prepared. Size is {len(target_funds)}")



# ---------- scrape from moneycontrol.com using our ISINs ---------- #
url = "https://api.moneycontrol.com/swiftapi/v1/mutualfunds/holdings"
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
headers = {"User-Agent": agent}


for fund in target_funds:
    isin = fund['ISIN']
    scheme_name = fund['Scheme NAV Name']

    file_path = f"fund_data/{isin}.json"
    if os.path.exists(file_path):
        print(f"ISIN {isin} already exists. Skipping.")
        continue

    print(f"Fetching holdings for: {scheme_name} ({isin})...")

    try:
        params = {"isin": isin, "deviceType": "W", "responseType": "json"}
        r = requests.get(url, params=params, headers=headers, timeout=10)

        if r.status_code == 200:
            data = r.json()
            stocks_list = data.get('data', {}).get('stock', [])

            processed_holdings = []
            for item in stocks_list:
                try:
                    weight = float(item.get('weighting', '0').replace(',', ''))
                except:
                    weight = 0.0
                
                processed_holdings.append({
                    "name": item.get('name'),
                    "weight": weight,
                    "sector": item.get('sector') or "Other"
                })

            # save to json
            output = {
                "isin": isin,
                "scheme_name": scheme_name,
                "holdings": processed_holdings
            }

            with open(file_path, 'w') as f:
                json.dump(output, f, indent=4)
        
        else:
            print(f"Error {r.status_code} for {isin}")    

    except Exception as e:
        print(f"Failed to process {isin}: {e}")

    # rate limiting to hopefully not get ip-banned
    time.sleep(random.uniform(2.0, 5.0))

print("Batch processing complete.")
