from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import pandas as pd
from pdfupload import database_new_v3


endpoint = "https://eastus.api.cognitive.microsoft.com/"
key = "f31a11c8e5694d8b9fc66dc7553b5f98"

model_id = "spira_power_v4"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
source='page_1.jpeg'
# with open(source, "rb") as pdf_file:
#     poller = document_analysis_client.begin_analyze_document(model_id, pdf_file)
#     result = poller.result()

# desired_keywords = ['Material', 'Thickness', 'Heat No.']

# row_data=[]
# for i, table in enumerate(result.tables):
#     # Check if any of the desired keywords are present in the table cells
#     if any(keyword.lower() in cell.content.lower() for keyword in desired_keywords for cell in table.cells):
#         columns = []
#         rows = []
#         for cell in table.cells:
#             if cell.column_index >= len(columns):
#                 columns.extend([None] * (cell.column_index - len(columns) + 1))
#             if cell.row_index >= len(rows):
#                 rows.extend([[]] * (cell.row_index - len(rows) + 1))
#             columns[cell.column_index] = cell.content
#             rows[cell.row_index].append(cell.content)
#         row_data.append(rows)
# database_new_v3.get_list(row_data)

def img_text_azure(source):
    with open(source, "rb") as pdf_file:
        poller = document_analysis_client.begin_analyze_document(model_id, pdf_file)
        result = poller.result()

    desired_keywords = ['Material', 'Thickness', 'Heat No.']

    row_data=[]
    for i, table in enumerate(result.tables):
        # Check if any of the desired keywords are present in the table cells
        if any(keyword.lower() in cell.content.lower() for keyword in desired_keywords for cell in table.cells):
            columns = []
            rows = []
            for cell in table.cells:
                if cell.column_index >= len(columns):
                    columns.extend([None] * (cell.column_index - len(columns) + 1))
                if cell.row_index >= len(rows):
                    rows.extend([[]] * (cell.row_index - len(rows) + 1))
                columns[cell.column_index] = cell.content
                rows[cell.row_index].append(cell.content)
            row_data.append(rows)
    database_new_v3.get_list(row_data)








