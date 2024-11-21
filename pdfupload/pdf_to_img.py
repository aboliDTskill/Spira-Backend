import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from pdfupload import azure_python_v3


def crop_pdf_pages_with_text(pdf_path, output_folder, texts_to_detect):

     # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # Convert each page of the PDF to images
    pages = convert_from_path(pdf_path)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # Iterate through each page
    for i, page in enumerate(pages):
        # Use pytesseract to extract text from the page
        print(type(page),'---------------------')
        pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
        print("hellllllllllllllllllllllllllllllllll")
        text_1 = pytesseract.image_to_string(page)
        # print('---23---',text_1,'---------',texts_to_detect,'----')
        
        # Check if any of the desired texts are present in the extracted text
        if any(text_to_detect in text_1 for text_to_detect in texts_to_detect):
            # Crop the image to the bounding box of the page
            cropped_img = page.crop(page.getbbox())
            
            # Save the cropped image
            output_path = os.path.join(output_folder, f"page_{i + 1}.jpeg")
            # print(output_path,'----------31---pdf_to_img----')
            cropped_img.save(output_path,'JPEG',quality=100)
        else:
            print('else')


def fetch_jpeg_images(root_folder):
    jpeg_images = []
    # Iterate through all folders and subfolders
    for folder_name, subfolders, filenames in os.walk(root_folder):
        # Sort filenames in ascending order
        filenames.sort()
        # Iterate through all files in the current folder
        for filename in filenames:
            # Check if the file is a JPEG image
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                # Construct the full path to the JPEG image
                image_path = os.path.join(folder_name, filename)
                print('------------',image_path,'----------')
                # Add the image path to the list of JPEG images
                azure_python_v3.img_text_azure(image_path)


# fetch_jpeg_images('output_image')





# main_output_folder = "output_image"
# texts_to_detect = ["Chemical Composition (%)", 'Mechanical Properties']
# crop_pdf_pages_with_text('C:/Users/bot/Downloads/Server_Pdf/Server_Pdf/pdf_extraction.pdf', main_output_folder,texts_to_detect)