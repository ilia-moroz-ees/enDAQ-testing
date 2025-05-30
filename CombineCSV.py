import os
import pandas as pd
import argparse

"""
A script for combining multiple CSV files into one horizontally
"""

def contains_keyword(column_name, keywords):
    return any(keyword.lower() in str(column_name).lower() for keyword in keywords)

def process_csv_files(directory):
    # Initialize an empty DataFrame to hold the combined data
    combined_data = pd.DataFrame()

    # Loop through all CSV files in the provided directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            
            # Read CSV without any special processing
            df = pd.read_csv(file_path)
            
            # Concatenate columns horizontally
            combined_data = pd.concat([combined_data, df], axis=1)

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
