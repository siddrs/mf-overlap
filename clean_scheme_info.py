import pandas as pd

input_file = "./data/scheme_info.csv"
output_file = "./data/cleaned_scheme_info.csv"
df = pd.read_csv(input_file)

nav_col = 'Scheme NAV Name'
isin_col = df.columns[3]

# keep only the direct growth plans
mask_name = (
    df[nav_col].str.contains('Direct', case=False, na=False) &
    df[nav_col].str.contains('Growth', case=False, na=False) &
    ~df[nav_col].str.contains('IDCW', case=False, na=False)
)

# we remove entries which have isins > 12 characters and also where the isin is missing
mask_isin = (
    df[isin_col].notna() & (df[isin_col].astype(str).str.strip().str.len() <= 12)
)

filtered_df = df[mask_name & mask_isin]

filtered_df.to_csv(output_file, index=False)

print(f"Filtering complete. Islotated {len(filtered_df)} Direct Growth plans")


