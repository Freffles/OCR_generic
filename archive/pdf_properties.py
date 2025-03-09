"""
This module extracts properties from PDF files, including metadata, page count, and image information.
It can process all PDF files in a specified folder and write the extracted properties to a CSV file.
"""
import os
import csv
import fitz  # PyMuPDF: Library for extracting and analyzing PDF content

def extract_pdf_properties(pdf_path):
    """
    Extract metadata, page count, and image information from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict: A dictionary containing:
            - filename: Name of the PDF file.
            - number_of_pages: Total page count in the PDF.
            - is_encrypted: Boolean indicating if the PDF is encrypted.
            - metadata: PDF metadata such as title, author, etc.
            - images_info: A list of dictionaries with image details:
                - page: Page number where the image is found.
                - xref: Reference ID of the image.
                - width: Image width in pixels.
                - height: Image height in pixels.
                - bpp: Bits per component (image quality).
                - colorspace: Colorspace of the image.
    """
    doc = fitz.open(pdf_path)  # Open the PDF file
    properties = {
        "filename": os.path.basename(pdf_path),  # Extract the filename
        "number_of_pages": doc.page_count,  # Get the total number of pages
        "is_encrypted": doc.is_encrypted,  # Check if the PDF is encrypted
        "metadata": doc.metadata,  # Extract PDF metadata
        "images_info": []  # Initialize a list to hold image information
    }

    # If the PDF is not encrypted, extract images and their details
    if not doc.is_encrypted:
        for page_num in range(doc.page_count):
            page = doc[page_num]  # Access each page
            image_list = page.get_images(full=True)  # Get all images on the page

            # Process each image found on the page
            for img in image_list:
                xref = img[0]  # Image reference ID
                img_info = doc.extract_image(xref)  # Extract image information
                properties["images_info"].append({
                    "page": page_num + 1,  # Page number (1-based index)
                    "xref": xref,
                    "width": img_info['width'],  # Image width
                    "height": img_info['height'],  # Image height
                    "bpp": img_info['bpc'],  # Bits per component (image quality)
                    "colorspace": img_info['colorspace']  # Image colorspace
                })
    doc.close()  # Close the PDF document
    return properties

def process_pdfs_in_folder(folder_path):
    """
    Process all PDF files in a specified folder and extract their properties.

    Args:
        folder_path (str): Path to the folder containing PDF files.

    Returns:
        list: A list of dictionaries, each containing properties of a PDF file.
    """
    pdf_properties_list = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):  # Process only PDF files
            pdf_path = os.path.join(folder_path, filename)
            properties = extract_pdf_properties(pdf_path)  # Extract PDF properties
            pdf_properties_list.append(properties)  # Add to the list
    return pdf_properties_list

def write_properties_to_csv(pdf_properties_list, csv_filename):
    """
    Write the extracted PDF properties to a CSV file.

    Args:
        pdf_properties_list (list): A list of dictionaries with PDF properties.
        csv_filename (str): Path to the output CSV file.

    Returns:
        None
    """
    # Define the header row for the CSV file
    header = [
        "filename",
        "number_of_pages",
        "is_encrypted",
        "title",
        "author",
        "subject",
        "creator",
        "producer",
        "creation_date",
        "mod_date",
        "page_number",
        "image_width",
        "image_height",
        "image_bpp",
        "image_colorspace"
    ]

    # Write data to the CSV file
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header row

        # Iterate through each PDF's properties
        for properties in pdf_properties_list:
            # Extract basic file information
            row_base = [
                properties["filename"],
                properties["number_of_pages"],
                properties["is_encrypted"],
                properties["metadata"].get("title", ""),  # Title metadata
                properties["metadata"].get("author", ""),  # Author metadata
                properties["metadata"].get("subject", ""),  # Subject metadata
                properties["metadata"].get("creator", ""),  # Creator metadata
                properties["metadata"].get("producer", ""),  # Producer metadata
                properties["metadata"].get("creationDate", ""),  # Creation date
                properties["metadata"].get("modDate", "")  # Modification date
            ]

            # If images are found, write image-specific information
            if properties["images_info"]:
                for image_info in properties["images_info"]:
                    row = row_base + [
                        image_info["page"],  # Page number
                        image_info["width"],  # Image width
                        image_info["height"],  # Image height
                        image_info["bpp"],  # Bits per component
                        image_info["colorspace"]  # Image colorspace
                    ]
                    writer.writerow(row)
            else:
                # If no images are found, write a single row with blank image details
                writer.writerow(row_base + ["", "", "", "", ""])

# Example usage
if __name__ == "__main__":
    # This is the main section of the script.
    # It defines the folder path and CSV file path.
    # Before running this script, make sure to install the required libraries:
    # pip install PyMuPDF
    folder_path = "pdf"  # Path to the folder containing PDF files
    csv_filename = "file_info.csv"  # Output CSV file path

    # Process PDFs and extract properties
    pdf_properties_list = process_pdfs_in_folder(folder_path)
    # Write the extracted properties to a CSV file
    write_properties_to_csv(pdf_properties_list, csv_filename)
    print(f"PDF properties have been written to {csv_filename}")
