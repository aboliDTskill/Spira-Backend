sudo apt-get update
sudo apt-get install -y unoconv

used above command for download docx api



otherwise we can use this code 
pip install aspose-words
import aspose.words as aw

def convert_docx_to_pdf(input_file: str, output_file: str):
    try:
        doc = aw.Document(input_file)
        doc.save(output_file, aw.SaveFormat.PDF)
        print(f"Conversion successful. PDF saved as {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None

def doc_file(sample_data):
    print(sample_data)
    # Your logic for doc_templete_create_v1.main_start(sample_data)

    input_file = "samp_output.docx"
    output_file = "samp_pdf_output.pdf"

    # Convert DOCX to PDF
    convert_docx_to_pdf(input_file, output_file)

    try:
        with open(output_file, 'rb') as file:
            pdf_data = file.read()
        pdf_bytes = bytes(pdf_data)
        return pdf_bytes
    except Exception as e:
        print(f"Failed to read the PDF file: {e}")
        return None






installed tesseract also


sudo apt-get install -y wkhtmltopdf        used this command for get feedback api



change the path of tesseract in production

i have added get all feedback api also



changed the quote file code