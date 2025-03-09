"""
This script reads data from an Excel file, adds a date column, and converts the data to a Markdown table,
which is then saved to a text file.
"""
import pandas as pd
from datetime import datetime

# Step 1: Read the Excel file, specifying the header row, sheet name, and usecols to start from column D
file_name = 'speedbumps.xlsx'
sheet_name = 'Sheet1'
df = pd.read_excel(file_name, sheet_name=sheet_name, header=2, usecols='D:F')  # Header is row 3 (index 2), usecols starts from column D

# Rename the columns to match the desired headings
df.columns = ['Topic', 'Issue', 'Resolution']

# Step 2: Add the Date column with the current date
current_date = datetime.now().strftime('%d-%b-%Y')
df['Date'] = current_date

# Step 3: Convert DataFrame to Markdown table format
markdown_table = df.to_markdown(index=False)

# Step 4: Save the Markdown table to a text file
output_file = 'speedbump.txt'
with open(output_file, 'w') as file:
    file.write(markdown_table)

print("Data has been extracted and saved to speedbump.txt")
