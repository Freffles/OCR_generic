"""
This script processes CSV files in a specified folder to remove unnecessary rows
from the beginning of each file. It searches for a row starting with 'Lvl' or
'Structure Level' and keeps only the rows from that point onwards. Files where
the search string is not found are logged in an error file.
"""
import os
import pandas as pd

# Define the folder containing the CSV files to be processed.
csv_folder = r'C:\Data\CSV_Temp'

# Define the path to the error log file where filenames with missing search strings will be recorded.
error_log_path = 'csv_error.txt'

# Open the error log file in append mode. This allows adding new errors without overwriting previous logs.
with open(error_log_path, mode='a') as error_log:
    
    # Iterate through each file in the specified CSV folder.
    for filename in os.listdir(csv_folder):
        # Process only files that end with the .csv extension.
        if filename.endswith('.csv'):
            # Construct the full path to the CSV file.
            file_path = os.path.join(csv_folder, filename)

            try:
                # Read the CSV file into a pandas DataFrame without a header, preserving the original data.
                df = pd.read_csv(file_path, header=None)
                
                # Define the strings to search for at the beginning of a row.
                search_str_1 = 'Lvl'
                search_str_2 = 'Structure Level'
                
                # Initialize a variable to store the index of the found row.
                found_index = None
                # Iterate through each row of the DataFrame along with its index.
                for i, row in df.iterrows():
                    # Check if the first element of the row starts with either of the search strings.
                    if str(row[0]).startswith(search_str_1) or str(row[0]).startswith(search_str_2):
                        # If a match is found, store the index and break the loop.
                        found_index = i
                        break
                
                # If the search string was found in the file.
                if found_index is not None:
                    # Create a new DataFrame containing only the rows from the found index onwards.
                    df_cleaned = df.iloc[found_index:].reset_index(drop=True)
                    
                    # Save the cleaned DataFrame back to the original CSV file path,
                    # without writing the index or header.
                    df_cleaned.to_csv(file_path, index=False, header=False)
                    # Print a success message.
                    print(f'Processed and cleaned: {filename}')
                else:
                    # If the search string was not found, log the filename to the error log.
                    error_log.write(f'{filename}\n')
                    # Print a message indicating that the search string was not found.
                    print(f'Search string not found in: {filename}')
            
            except Exception as e:
                # Print an error message if any issue occurs during file processing.
                print(f'Error processing {file_path}: {e}')
