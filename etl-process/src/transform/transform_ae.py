import pandas as pd
import os
import glob

# Paths
raw_dir = "../data/raw"
pro_dir = "../data/processed"

# Recursively find all A&E CSVs
ae_files = glob.glob(os.path.join(raw_dir, "**", "ae_*.csv"), recursive=True)
print(f"Found {len(ae_files)} files:")
print(ae_files)

if not ae_files:
    print("No files found. Check folder structure or filenames.")
else:
    # Read each CSV into a dataframe
    ae_df_list = [pd.read_csv(f) for f in ae_files]
    
    # Combine all dataframes into one
    ae_data = pd.concat(ae_df_list, ignore_index=True)
    
    # Quick checks
    print("Combined data shape:", ae_data.shape)
    print("Columns:", ae_data.columns.tolist())
    print(ae_data.head())
