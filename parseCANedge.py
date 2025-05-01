import os
import sys
import re
from asammdf import MDF
from pathlib import Path
import pandas as pd
from filterCSVData import process_csv_files
import shutil  # Import shutil for moving files

def get_long_path(path):
    """ Convert to long path format on Windows to handle long file paths. """
    if os.name == 'nt' and not path.startswith('\\\\?\\'):
        return f"\\\\?\\{os.path.abspath(path)}"
    return path

def convert_wsl_to_windows_path(wsl_path):
    """Convert a WSL path to a Windows-accessible path."""
    if wsl_path.startswith('/mnt/'):
        drive_letter = wsl_path[5].upper()
        windows_path = f"{drive_letter}:\\{wsl_path[7:].replace('/', '\\')}"
        return windows_path
    elif wsl_path.startswith('\\wsl.localhost'):
        # No conversion needed for WSL UNC paths; just return it.
        return wsl_path
    else:
        return wsl_path

def rename_csv_files(folder_path):
    # Prepare the folder path for long path handling on Windows
    folder_path = get_long_path(folder_path)

    # List all CSV files in the specified folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Regex patterns to match different filename formats
    pattern1 = re.compile(r'CAN\d+_ID=(0x[0-9A-Fa-f]+)_(.*?)_PGN.*?\.csv', re.IGNORECASE)
    pattern2 = re.compile(r'ChannelGroup_\d+_CAN\d+_-_message_(.*?)_(0x[0-9A-Fa-f]+)_EXT.*?\.csv', re.IGNORECASE)

    for csv_file in csv_files:
        # Prepare the file path for long path handling on Windows
        csv_file_path = get_long_path(os.path.join(folder_path, csv_file))

        # Attempt to match pattern 1
        match1 = pattern1.search(csv_file)
        if match1:
            can_id = match1.group(1)
            signal_name = match1.group(2)
            new_name = f"{can_id}_{signal_name}.csv"

        # Attempt to match pattern 2
        else:
            match2 = pattern2.search(csv_file)
            if match2:
                signal_name = match2.group(1)
                can_id = match2.group(2)
                new_name = f"{can_id}_{signal_name}.csv"
            else:
                print(f"Skipped '{csv_file}' - No matching pattern found.")
                continue

        # Prepare the new file path for long path handling on Windows
        new_path = get_long_path(os.path.join(folder_path, new_name))

        # Check for existing file with new name and handle accordingly
        if os.path.exists(new_path):
            # Delete the old file if the new file name already exists
            print(f"Deleting '{csv_file}' as '{new_name}' already exists.")
            os.remove(csv_file_path)
        else:
            # Rename the file
            os.rename(csv_file_path, new_path)
            print(f"Renamed '{csv_file}' to '{new_name}'")
            
def combine_and_decode_mf4(source_folder, dbc_paths):
    # Prepare the source folder path for long path handling on Windows
    source_folder = get_long_path(source_folder)
    
    # Convert WSL paths to Windows paths if necessary
    dbc_paths = [convert_wsl_to_windows_path(i) for i in dbc_paths]
    dbc_paths = [get_long_path(i) for i in dbc_paths]

    # Collect all MF4 files in the source folder recursively
    mf4_files = [str(file) for file in Path(source_folder).rglob('*.mf4')]

    print(f"Number of MF4 files found in {source_folder}: {len(mf4_files)}")
    print(mf4_files)
    
    # Determine the output folder and file paths
    decoded_folder = source_folder.replace('encoded', 'decoded')
    decoded_folder = get_long_path(decoded_folder)  # Ensure long path handling
    if not os.path.exists(decoded_folder):
        os.makedirs(decoded_folder)
    
    output_mf4_path = get_long_path(os.path.join(decoded_folder, 'decoded.mf4'))
    output_csv_path = get_long_path(os.path.join(decoded_folder, 'CSVs'))

    # Combine MF4 files if there's more than one, otherwise just use the single file
    if len(mf4_files) > 1:
        print(f"Merging all .mf4 files into one.")
        combined_mdf = MDF.concatenate([MDF(f) for f in mf4_files], sync=False, version='4.0.0')
    elif len(mf4_files) == 1:
        combined_mdf = MDF(mf4_files[0])
    else:
        print("No MF4 files found in the specified folder.")
        sys.exit(1)

    # Setup database files dictionary for CAN bus
    database_files = {
        "CAN": [(i, 0) for i in dbc_paths],  # 0 specifies any bus channel
    }
    print(database_files)
    
    print(f"Decoding .mf4 files using: {dbc_paths}")
    # Decode using the provided DBC file with extract_bus_logging
    combined_mdf = combined_mdf.extract_bus_logging(
        database_files=database_files,
        version='4.0.0',
        ignore_value2text_conversion=True,
    )

    # Save the decoded MDF file
    # combined_mdf.save(output_mf4_path)

    # Convert the MDF data to CSV with a normal timestamp format
    combined_mdf.export(fmt='csv', filename=output_csv_path, time_as_date=True)

    print(f"Decoded MDF saved at: {output_mf4_path}. You can view this in asammdf.")
    print(f"CSV exports saved in: {output_csv_path}.")

    # Rename CSVs to be more human-readable, remove logs of messages repeated on multiple files
    print(f"Giving CSV files more human-readable names and removing duplicate message logs...")
    rename_csv_files(decoded_folder)

    # Filter data of interest out of csv files and into a master csv file
    # print(f"Creating master.csv with filtered data of interest...")
    # process_csv_files(decoded_folder)

    # Create subfolders for CSVs and plots
    csv_folder = os.path.join(decoded_folder, 'csv')
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Move CSV files to the 'csv' folder and plots (.png and .mat files) to the 'plots' folder
    for file in os.listdir(decoded_folder):
        file_path = os.path.join(decoded_folder, file)
        if file.endswith('.csv'):
            shutil.move(file_path, os.path.join(csv_folder, file))

    print(f"CSV files moved to: {csv_folder}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parseCanedge.py <source_folder> [<dbc_file>]")
        sys.exit(1)

    source_folder = sys.argv[1]

    # Check if the second argument (dbc_file) is provided

    dbc_files = sys.argv[2:]

    combine_and_decode_mf4(source_folder, dbc_files)
