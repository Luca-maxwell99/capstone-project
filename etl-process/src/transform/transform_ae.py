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

# -----------------------
# STEP 2: Read and combine CSVs
# -----------------------
ae_df_list = [pd.read_csv(f) for f in ae_files]
ae_data = pd.concat(ae_df_list, ignore_index=True)
print("Combined dataframe shape:", ae_data.shape)

# Strip whitespace from column names
ae_data.columns = ae_data.columns.str.strip()

# -----------------------
# STEP 3: Rename columns (unify naming across all CSVs)
# -----------------------
rename_map = {
    # Period
    "Period": "period",
    "Reporting Period": "period",

    # Org Code
    "Org Code": "org_code",
    "Organisation Code": "org_code",

    # Org Name
    "Org name": "org_name",
    "Organisation Name": "org_name",

    # Attendances (Type 1)
    "Number of A&E attendances Type 1": "ae_attendances_type_1",
    "A&E attendances Type 1": "ae_attendances_type_1",

    # Attendances over 4hrs (Type 1)
    "Number of attendances over 4hrs Type 1": "attendances_over_4hrs_type_1",
    "Attendances over 4hrs Type 1": "attendances_over_4hrs_type_1",

    # 12hr waits
    "Patients who have waited 12+ hrs from DTA to admission": "patients_12hr_wait",
    "12 hour waits": "patients_12hr_wait",

    # Emergency admissions (Type 1)
    "Emergency admissions via A&E - Type 1": "emergency_admissions_type_1",
    "Emergency Admissions Type 1": "emergency_admissions_type_1",
}

# Keep only existing columns for renaming
existing_rename_map = {k: v for k, v in rename_map.items() if k in ae_data.columns}
missing_cols = [k for k in rename_map.keys() if k not in ae_data.columns]

if missing_cols:
    print("WARNING: These columns were not found and will be skipped:")
    for col in missing_cols:
        print(f"- {col}")

ae_data = ae_data.rename(columns=existing_rename_map)

# -----------------------
# STEP 3b: Merge duplicate columns (keep all data, no NaNs)
# -----------------------
for col in ae_data.columns[ae_data.columns.duplicated()]:
    duplicate_cols = [c for c in ae_data.columns if c == col]
    # Fill missing values from the next duplicate column
    ae_data[col] = ae_data[duplicate_cols].bfill(axis=1).iloc[:, 0]

# Remove now-merged duplicate columns
ae_data = ae_data.loc[:, ~ae_data.columns.duplicated()]

# -----------------------
# STEP 4: Parse period column
# -----------------------
if 'period' in ae_data.columns:
    ae_data['period'] = ae_data['period'].str.upper()  # normalize text
    month_map = {
        'JANUARY': '01', 'FEBRUARY': '02', 'MARCH': '03', 'APRIL': '04',
        'MAY': '05', 'JUNE': '06', 'JULY': '07', 'AUGUST': '08',
        'SEPTEMBER': '09', 'OCTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'
    }

    def parse_period(x):
        try:
            for month_name, month_num in month_map.items():
                if month_name in x:
                    year = x.split('-')[-1]
                    return pd.Timestamp(f"{year}-{month_num}-01")
            return pd.NaT
        except:
            return pd.NaT

    ae_data['period'] = ae_data['period'].apply(parse_period)
    missing_dates = ae_data['period'].isna().sum()
    print(f"Rows with unparsed periods: {missing_dates}")
else:
    print("No 'period' column to parse!")

# -----------------------
# STEP 5: Keep only required columns
# -----------------------
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
cleaned_ae_data = ae_data[existing_cols_to_keep]

# Drop duplicates
cleaned_ae_data = cleaned_ae_data.drop_duplicates()

# Sort by period
cleaned_ae_data = cleaned_ae_data.sort_values("period").reset_index(drop=True)

print("Cleaned dataframe shape after dropping duplicates and sorting:", cleaned_ae_data.shape)

# -----------------------
# STEP 6: Ensure processed folder exists
# -----------------------
os.makedirs(PROCESSED_DIR, exist_ok=True)

# -----------------------
# STEP 7: Save cleaned data
# -----------------------
output_file = os.path.join(PROCESSED_DIR, "ae_data_cleaned.csv")
cleaned_ae_data.to_csv(output_file, index=False)
print(f"Cleaned A&E data saved to {output_file}")
