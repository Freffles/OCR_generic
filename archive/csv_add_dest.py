"""
This script inserts a "Source" column into each CSV file located in the specified folder.
The value for the "Source" column is derived from the original filename of the CSV file.
"""
import os
import pandas as pd
import csv

# Define the path to the CSV file ('output_file.csv') which contains a list of file paths.
# This file is expected to have a column named 'File Path'.
output_csv_path = 'output_file.csv'

# Define the folder where the converted CSV files are stored.
csv_save_folder = r'C:\Data\CSV_Temp'

# Create the directory for saving CSV files if it does not exist.
if not os.path.exists(csv_save_folder):
    os.makedirs(csv_save_folder)

# Open the output CSV file that contains the list of file paths.
with open(output_csv_path, mode='r') as file:
    # Create a DictReader object to read the CSV file as dictionaries.
    reader = csv.DictReader(file)
    
    # Iterate over each row in the output CSV file.
    for row in reader:
        # Extract the file path from the 'File Path' column of the current row.
        file_path = row['File Path']
        
        # Extract the base filename (without extension) from the file path.
        original_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # Construct the full path to the corresponding CSV file in the save folder.
        csv_file_path = os.path.join(csv_save_folder, f'{original_filename}.csv')
        
        # Check if the converted CSV file exists.
        if os.path.isfile(csv_file_path):
            try:
                # Read the CSV file into a pandas DataFrame.
                csv_data = pd.read_csv(csv_file_path)
                
                # Insert a new column named "Source" at the beginning of the DataFrame.
                # The value for each row in this column is set to the original filename.
                csv_data.insert(0, 'Source', original_filename)
                
                # Save the updated DataFrame back to the CSV file, without including the index.
                csv_data.to_csv(csv_file_path, index=False)
                
                # Print a success message indicating the file has been processed.
                print(f'Successfully added Source column and saved: {csv_file_path}')
            except Exception as e:
                # Print an error message if any issue occurs during file processing.
                print(f'Error processing file {csv_file_path}: {e}')
        else:
            # Print a message if the corresponding CSV file is not found.
            print(f'CSV file not found: {csv_file_path}')
