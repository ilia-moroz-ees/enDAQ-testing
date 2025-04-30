import os
import pandas as pd
from datetime import datetime
import argparse
import re

# Hardcoded list of headers of interest, disregarding CAN1 or CAN2 prefixes
headers_of_interest = [
    "FORIPOWER_DCDC_status1.DCDC_Output_Current",
    "FORIPOWER_DCDC_status1.DCDC_Output_Voltage",
    "FORIPOWER_DCDC_status1.DCDC_Temperature",
    "TCCI_COMPRESSOR1_status.ECTrnstrTemp", 
    "TCCI_COMPRESSOR1_status.ECSpeedFdbk",
    "TCCI_COMPRESSOR1_status.ECDCCurrent",
    "TCCI_COMPRESSOR1_status.ECDCVoltage",
    "TCCI_COMPRESSOR2_status.ECTrnstrTemp",
    "TCCI_COMPRESSOR2_status.ECSpeedFdbk",
    "TCCI_COMPRESSOR2_status.ECDCCurrent",
    "TCCI_COMPRESSOR2_status.ECDCVoltage",
    "DIAGNOSTICS_INTERNAL_VARIABLES.SystemLoad",
    "DIAGNOSTICS_LOOP_1_OUTPUTS.PumpSpeedRequest",
    "DIAGNOSTICS_LOOP_1_OUTPUTS.CompressorSpeedRequest",
    "DIAGNOSTICS_LOOP_1_OUTPUTS.FanSpeedRequest",
    "DIAGNOSTICS_LOOP_2_OUTPUTS.PumpSpeedRequest",
    "DIAGNOSTICS_LOOP_2_OUTPUTS.CompressorSpeedRequest",
    "DIAGNOSTICS_LOOP_2_OUTPUTS.FanSpeedRequest",
    "DIAGNOSTICS_COMMON_INPUTS_2.AmbientTemperature"

    # Add more headers as needed
]

def process_csv_files(directory):
    # Initialize an empty DataFrame to hold the combined data
    combined_data = pd.DataFrame()

    # Loop through all CSV files in the provided directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            # Read the CSV file
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # Convert timestamps to milliseconds since the first timestamp
            first_timestamp = pd.to_datetime(df.iloc[0, 0], format='mixed')
            df['timestamp_ms'] = ((pd.to_datetime(df.iloc[:, 0], format='mixed') - first_timestamp).dt.total_seconds() * 1000).round()

            # Loop through each header of interest
            for header in headers_of_interest:
                # Match headers regardless of CAN1 or CAN2 prefixes
                regex_pattern = rf"CAN\d+\.{re.escape(header)}"
                matched_columns = [col for col in df.columns if re.match(regex_pattern, col)]

                # If the header exists in the current CSV
                if matched_columns:
                    matched_column = matched_columns[0]  # Use the first match found
                    # Create a new DataFrame for this pair
                    filtered_df = df[['timestamp_ms', matched_column]].dropna()

                    # Rename columns to include both timestamp and data columns for this header
                    new_columns = [f'timestamp_ms for {header}', matched_column]
                    filtered_df.columns = new_columns

                    # Append the pair to the combined data (side-by-side)
                    if combined_data.empty:
                        combined_data = filtered_df
                    else:
                        combined_data = pd.concat([combined_data, filtered_df], axis=1)

    # Save the combined data to 'master.csv' in the source directory
    try:
        master_csv_filepath = os.path.join(directory, 'master.csv')
        combined_data.to_csv(master_csv_filepath, index=False)
    except:
        print("Unable to open " + master_csv_filepath + " for writing. Ensure this file is not open in any other editor")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process CSV files and extract columns of interest.")
    parser.add_argument("directory", type=str, help="Path to the directory containing the CSV files.")
    args = parser.parse_args()

    # Process the CSV files in the provided directory
    process_csv_files(args.directory)

if __name__ == "__main__":
    main()
