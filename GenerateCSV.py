import pytesseract
import textract
import re
import csv
import os
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Needs ImageMagick installed, tesseract, textract, pytesseract

def ocr_pdf(file_path):
    text = textract.process(file_path, method='tesseract', language='eng')
    return text.decode('utf-8')

def extract_data_with_regex(pdf_text):
    # Modify these patterns according to your specific requirements
    floor_area_regex = r"Total floor area (\d+) square metres"
    energy_rating_regex = r"This property's current energy rating is ([A-G])"
    address_regex = r"(\d+ [\w\s]+)\n([\w\s]+)\n([A-Z0-9]+ [A-Z0-9\s]+)"
    property_type_regex = r"Property type (\w+-?\w+ \w+)"
    potential_rating_regex = r"the potential to be ([A-G])"
    energy_usage_regex = r"The primary energy use for this property per year is (\d+) kilowatt hours per square metre \(kWh/m2\)"
    
    # Search for the data using regex
    floor_area_match = re.search(floor_area_regex, pdf_text)
    energy_rating_match = re.search(energy_rating_regex, pdf_text)
    address_match = re.search(address_regex, pdf_text)
    property_type_match = re.search(property_type_regex, pdf_text)
    potential_rating_match = re.search(potential_rating_regex, pdf_text)
    energy_usage_match = re.search(energy_usage_regex, pdf_text)
    
    # Extract the matched values
    floor_area = floor_area_match.group(1) if floor_area_match else None
    energy_rating = energy_rating_match.group(1) if energy_rating_match else None
    address_line1 = address_match.group(1).strip() if address_match else None
    address_line2 = address_match.group(2).strip() if address_match else None
    postcode = address_match.group(3).strip() if address_match else None
    property_type = property_type_match.group(1) if property_type_match else None
    potential_rating = potential_rating_match.group(1) if potential_rating_match else None
    energy_usage = energy_usage_match.group(1) if energy_usage_match else None
    
    # Return the extracted data as a dictionary
    extracted_data = {
        'Floor Area': floor_area,
        'Energy Rating': energy_rating,
        'Address Line 1': address_line1,
        'Address Line 2': address_line2,
        'Postcode': postcode,
        'Property Type': property_type,
        'Potential Rating': potential_rating,
        'Primary Energy Usage': energy_usage
    }
    
    return extracted_data

# Main script
pdf_folder = r'Edit Location Here'
csv_file = r'Edit Location Here'
text_file = r'Edit Location Here'
write_debug_text = True  # Set this to False to disable writing debug text

# Remove the existing CSV file if it already exists
if os.path.exists(csv_file):
    os.remove(csv_file)

# Remove the existing text file if it already exists
if os.path.exists(text_file):
    os.remove(text_file)

# Extracted data from all PDF files
all_data = []

# Debug text to store all extracted text from PDFs
debug_text = ''

# Iterate over PDF files in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        pdf_file = os.path.join(pdf_folder, filename)

        # OCR the PDF
        print(f"Performing OCR on: {filename}")
        pdf_text = ocr_pdf(pdf_file)

        # Append the extracted text to the debug text
        debug_text += f'--- {filename} ---\n'
        debug_text += pdf_text
        debug_text += '\n\n'

        # Extract data using regex
        extracted_data = extract_data_with_regex(pdf_text)

        # Append the extracted data to the list
        all_data.append(extracted_data)

# Write the debug text to the text file if enabled
if write_debug_text:
    with open(text_file, 'w') as file:
        file.write(debug_text)

# Write the extracted data to the CSV file
print('Writing data to CSV...')
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['Floor Area', 'Energy Rating', 'Address Line 1', 'Address Line 2', 'Postcode', 'Property Type', 'Potential Rating', 'Primary Energy Usage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print('Extraction complete. Data from all PDF files has been written to', csv_file)
