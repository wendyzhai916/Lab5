import os
from PyPDF2 import PdfReader
import mysql.connector
from pytesseract import image_to_string
from PIL import Image
import pytesseract
import ocrmypdf

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'<path_tesseract_executable>'

# Database connection details
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'lab05',
}

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file using PyPDF2.
    """
    text = ''
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() + ' '
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

def ocr_pdf_to_text(pdf_path):
    """
    Performs OCR on a PDF file using OCRmyPDF and PyTesseract, returning the extracted text.
    """
    ocr_output = pdf_path.replace('.pdf', '_ocr.pdf')
    ocrmypdf.ocr(pdf_path, ocr_output, deskew=True)
    return extract_text_from_pdf(ocr_output)

def insert_data_into_db(data):
    """
    Inserts extracted data into the MySQL database.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = ("INSERT INTO wells (api_number, longitude, latitude, well_name, address, stimulation_data) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to insert data into MySQL table: {err}")

def main():
    pdf_folder_path = '../../data/raw/'
    
    for pdf_file in os.listdir(pdf_folder_path):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, pdf_file)
            print(f"Processing {pdf_file}...")
            # Assuming the use of OCR for scanned PDFs
            text = ocr_pdf_to_text(pdf_path)
            # Parse the text to extract relevant data
            # This is a placeholder - actual parsing logic will depend on the PDF structure
            api_index = text.find('API: ') + len('API: ')
            long_index = text.find('Longitude: ') + len('Longitude: ')
            lat_index = text.find('Latitude: ') + len('Latitude: ')
            well_index = text.find('Well Name: ') + len('Well Name: ')
            address_index = text.find('(SHL:)')

            api = text[api_index:text.find(" ", api_index)]
            long = text[long_index:text.find(" ", long_index)]
            lat = text[lat_index:text.find(" ", lat_index)]
            well = text[well_index:text.find(" ", well_index)]
            address = text[address_index:text.find(" ", address_index)]
            
            data = (api, long, lat, well, address)
            # Insert the data into the database
            insert_data_into_db(data)

if __name__ == "__main__":
    main()
