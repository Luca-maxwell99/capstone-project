# transform_ae.py
import pandas as pd
import glob
import os

# -----------------------
# STEP 0: Paths (dynamic, project-root relative)
# -----------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

RAW_DIR = os.path.join(project_root, "data", "raw")
PROCESSED_DIR = os.path.join(project_root, "data", "processed")

print(f"Looking for raw CSVs in: {RAW_DIR}")
print(f"Processed data will be saved in: {PROCESSED_DIR}")

# -----------------------
# STEP 1: Find all A&E CSVs recursively
# -----------------------
ae_files = glob.glob(os.path.join(RAW_DIR, "**", "ae_*.csv"), recursive=True)
print(f"Found {len(ae_files)} A&E CSV files:")
print(ae_files)

if not ae_files:
    raise FileNotFoundError("No A&E CSV files found. Check folder structure or filenames.")

# Read and combine all CSVs
ae_df_list = [pd.read_csv(f) for f in ae_files]
ae_data = pd.concat(ae_df_list, ignore_index=True)
print("Combined dataframe shape:", ae_data.shape)

# Print the original columns to verify
print("Original columns in combined dataframe:")
for col in ae_data.columns:
    print(f"- {col}")

# --- Rename columns based on exact names in your CSV ---
rename_map = {
    "Period": "period",
    "Org Code": "org_code",
    "Org name": "org_name",
    "A&E attendances Type 1": "ae_attendances_type_1",
    "Attendances over 4hrs Type 1": "attendances_over_4hrs_type_1",
    "Patients who have waited 12+ hrs from DTA to admission": "patients_12hr_wait",
    "Emergency admissions via A&E - Type 1": "emergency_admissions_type_1"
}

# Check which columns exist before renaming
existing_rename_map = {k: v for k, v in rename_map.items() if k in ae_data.columns}
missing_cols = [k for k in rename_map.keys() if k not in ae_data.columns]

if missing_cols:
    print("WARNING: These columns were not found in the data and will be skipped:")
    for col in missing_cols:
        print(f"- {col}")

ae_data = ae_data.rename(columns=existing_rename_map)

# Convert 'period' to datetime
if 'period' in ae_data.columns:
    # Try format YYYY-MM first
    ae_data['period'] = pd.to_datetime(ae_data['period'], format='%Y-%m', errors='coerce')
    missing_dates = ae_data['period'].isna().sum()
    print(f"Rows with unparsed periods: {missing_dates}")
else:
    print("No 'period' column to parse!")

# Keep only the columns we care about
cols_to_keep = [
    "period",
    "org_code",
    "org_name",
    "ae_attendances_type_1",
    "attendances_over_4hrs_type_1",
    "patients_12hr_wait",
    "emergency_admissions_type_1"
]

existing_cols_to_keep = [col for col in cols_to_keep if col in ae_data.columns]
print("Columns to keep after checking existence:")
print(existing_cols_to_keep)

cleaned_ae_data = ae_data[existing_cols_to_keep]

# Drop duplicates
cleaned_ae_data = cleaned_ae_data.drop_duplicates()
print("Cleaned dataframe shape after dropping duplicates:", cleaned_ae_data.shape)

# Ensure processed folder exists
pro_dir = "data/processed"
os.makedirs(pro_dir, exist_ok=True)

# Save cleaned data
output_file = os.path.join(pro_dir, "ae_data_cleaned.csv")
cleaned_ae_data.to_csv(output_file, index=False)
print(f"Cleaned A&E data saved to {output_file}")