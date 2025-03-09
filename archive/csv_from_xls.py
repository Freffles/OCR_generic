"""
This script converts Excel files (with .xlsx extension) listed in the 'output_file.csv'
into individual CSV files and saves them in a specified directory.
"""
import os
import pandas as pd
import csv

# Define the path to the CSV file that contains a list of Excel file paths.
output_csv_path = 'output_file.csv'  # This CSV file should have a column named 'File Path'.

# Define the folder where the converted CSV files will be saved.
csv_save_folder = r'C:\Data\CSV_Temp'

# Create the directory for saving CSV files if it does not already exist.
if not os.path.exists(csv_save_folder):
    os.makedirs(csv_save_folder)

# Open the output CSV file containing the list of Excel file paths.
with open(output_csv_path, mode='r') as file:
    # Create a DictReader object to read the CSV file as dictionaries.
    reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file.
    for row in reader:
        # Extract the Excel file path from the 'File Path' column of the current row.
        file_path = row['File Path']
        
        # Check if the specified file path exists.
        if os.path.isfile(file_path):
            try:
                # Read the Excel file into a pandas DataFrame.
                excel_data = pd.read_excel(file_path)
                
                # Extract the base name of the Excel file without the extension.
                filename = os.path.splitext(os.path.basename(file_path))[0]
                
                # Construct the full path for the output CSV file.
                csv_file_path = os.path.join(csv_save_folder, f'{filename}.csv')
                
                # Save the DataFrame to a CSV file, without including the index.
                excel_data.to_csv(csv_file_path, index=False)
                
                # Print a success message indicating the conversion and save location.
                print(f'Successfully converted and saved: {csv_file_path}')
            except Exception as e:
                # Print an error message if any issue occurs during file processing.
                print(f'Error processing file {file_path}: {e}')
