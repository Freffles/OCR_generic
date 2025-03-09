"""
This script consolidates all CSV files located in the specified folder into a single master CSV file.
"""
import os
import pandas as pd

# Define the folder where the individual CSV files are stored.
csv_save_folder = r'C:\Data\CSV_Temp'

# Define the path for the consolidated master CSV file.
master_csv_path = 'cons_master.csv'

# Check if the master CSV file already exists. If it does, remove it to ensure a fresh consolidation.
if os.path.exists(master_csv_path):
    os.remove(master_csv_path)

# Iterate through each file in the specified directory.
for filename in os.listdir(csv_save_folder):
    # Process only files that end with the .csv extension.
    if filename.endswith('.csv'):
        # Construct the full path to the CSV file.
        csv_file_path = os.path.join(csv_save_folder, filename)
        
        try:
            # Read the CSV file into a pandas DataFrame.
            csv_data = pd.read_csv(csv_file_path)
            
            # Append the data from the current CSV file to the master CSV file.
            # The 'mode='a'' argument ensures that data is appended to the file.
            # 'header=True' ensures that headers are included in each appended CSV.
            # 'index=False' prevents the DataFrame index from being written to the CSV.
            csv_data.to_csv(master_csv_path, mode='a', header=True, index=False)
            
            # Print a success message to the console.
            print(f'Successfully appended: {filename}')
        
        except Exception as e:
            # If an error occurs during file processing, print an error message.
            print(f'Error processing file {csv_file_path}: {e}')
