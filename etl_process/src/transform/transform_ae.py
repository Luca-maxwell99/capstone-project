import pandas as pd
import glob
import os

def transform_ae_data():
    # Get the absolute path to the root of the project
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    # Define input and output folders for raw and processed data
    RAW_DIR = os.path.join(project_root, "data", "raw")
    PROCESSED_DIR = os.path.join(project_root, "data", "processed")

    print(f"Looking for raw CSVs in: {RAW_DIR}")
    print(f"Processed data will be saved in: {PROCESSED_DIR}")

    # Glob looks for any CSV starting with "ae_" inside raw data folders
    ae_files = glob.glob(os.path.join(RAW_DIR, "**", "ae_*.csv"), recursive=True)
    print(f"Found {len(ae_files)} A&E CSV files:")
    print(ae_files)

    # If no files are found this raises an error
    if not ae_files:
        raise FileNotFoundError("No A&E CSV files found. Check folder structure or filenames.")

    # Read each CSV into a DataFrame, then merge into one big DataFrame
    ae_df_list = [pd.read_csv(f) for f in ae_files]
    ae_data = pd.concat(ae_df_list, ignore_index=True)
    print("Combined dataframe shape:", ae_data.shape)

    # Strip whitespace from column names. Standardise the column names by removing trailing spaces
    ae_data.columns = ae_data.columns.str.strip()

    # Different CSVs may use slightly different headers so they are mapped to a standard schema
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

    # This loops over rename_map and only includes pairs where the key exists 
    existing_rename_map = {k: v for k, v in rename_map.items() if k in ae_data.columns}

    # This builds a list of keys that are not present
    missing_cols = [k for k in rename_map.keys() if k not in ae_data.columns]

    # And prints a warning if any expected columns are missing
    if missing_cols:
        print("WARNING: These columns were not found and will be skipped:")
        for col in missing_cols:
            print(f"- {col}")

    ae_data = ae_data.rename(columns=existing_rename_map)

    # Merge duplicate columns (keep all data, no NaNs)
    for col in ae_data.columns[ae_data.columns.duplicated()]:
        duplicate_cols = [c for c in ae_data.columns if c == col]
        # Fill missing values from the next duplicate column
        ae_data[col] = ae_data[duplicate_cols].bfill(axis=1).iloc[:, 0]

    # This drops duplicate columns after merging
    ae_data = ae_data.loc[:, ~ae_data.columns.duplicated()]
    

    if 'period' in ae_data.columns:
        ae_data['period'] = ae_data['period'].str.upper()  # normalise text to uppercase
        month_map = {
            'JANUARY': '01', 'FEBRUARY': '02', 'MARCH': '03', 'APRIL': '04',
            'MAY': '05', 'JUNE': '06', 'JULY': '07', 'AUGUST': '08',
            'SEPTEMBER': '09', 'OCTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'
        }

        # Try to convert date strings into timestamp
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

    # This defines the standardised schema we want to keep 
    cols_to_keep = [
        "period",
        "org_code",
        "org_name",
        "ae_attendances_type_1",
        "attendances_over_4hrs_type_1",
        "patients_12hr_wait",
        "emergency_admissions_type_1"
    ]

    # Drops any cols we don't want to keep
    existing_cols_to_keep = [col for col in cols_to_keep if col in ae_data.columns]
    cleaned_ae_data = ae_data[existing_cols_to_keep]

    # Drop duplicate rows 
    cleaned_ae_data = cleaned_ae_data.drop_duplicates()

    # Sort by period
    cleaned_ae_data = cleaned_ae_data.sort_values("period").reset_index(drop=True)

    print("Cleaned dataframe shape after dropping duplicates and sorting:", cleaned_ae_data.shape)

    # Ensure processed folder exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Save cleaned data
    output_file = os.path.join(PROCESSED_DIR, "ae_data_cleaned.csv")
    cleaned_ae_data.to_csv(output_file, index=False)
    print(f"Cleaned A&E data saved to {output_file}")

    '''
    this script finds all raw A&E data
    combines it into a single data frame
    standardises col names 
    parses period into datetime
    keeps the cols I care about
    drops duplicates and sorts chronologically
    and finally exports it to data/processed 
    '''

    return cleaned_ae_data
