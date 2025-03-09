"""
This script finds all the Excel files (with .xlsx extension) within a specified folder
and its sub-folders. It then extracts the filename and creation date of each Excel file
and writes this information to a CSV file named 'output_file.csv'.
"""
import os
import datetime
import csv

# Define the path to the folder that will be searched for Excel files.
folder_path = r"C:\Data\5BMaxUp"

# Define the path for the output CSV file where the file information will be saved.
csv_file_path = 'output_file.csv'

# Open the CSV file in write mode. The 'newline=''' argument prevents empty rows in the CSV.
with open(csv_file_path, mode='w', newline='') as file:
    # Create a CSV writer object.
    writer = csv.writer(file)
    
    # Write the header row to the CSV file.
    writer.writerow(['Filename', 'Creation Date'])
    
    # Iterate through each item (files and directories) in the specified folder.
    for filename in os.listdir(folder_path):
        # Construct the full file path by joining the folder path and the filename.
        file_path = os.path.join(folder_path, filename)
        
        # Check if the current path is a file (not a directory).
        if os.path.isfile(file_path):
            # Check if the file ends with the '.xlsx' extension, indicating it's an Excel file.
            if filename.endswith('.xlsx'):
                # Get the file's creation timestamp.
                creation_time = os.path.getctime(file_path)
                
                # Convert the creation timestamp to a human-readable date and time format.
                creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%A, %B %d, %Y %I:%M:%S %p')
                
                # Write the filename and its creation date to the CSV file.
                writer.writerow([filename, creation_date])

# Print a message to the console indicating that the output has been written to the CSV file.
print(f'Output has been written to {csv_file_path}')
