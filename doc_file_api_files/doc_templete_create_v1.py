# utils.py
from docxtpl import DocxTemplate

def string_1(string_values):
    final_dict = dict.fromkeys(string_values.split(', '), None)
    value_map = {
        "Quality": "a",
        "Trust": "b",
        "Brand Name": "c",
        "Previous experience": "d",
        "Word of mouth": "e"
    }
    for keyword in string_values.split(', '):
        if keyword in value_map:
            final_dict[keyword] = value_map[keyword]
    return final_dict

def string_2(string_values):
    final_dict = dict.fromkeys(string_values.split(', '), None)
    value_map = {
        "Customer Satisfaction": "f",
        "Response Time": "g",
        "Quality of product": "h",
        "Customer Engagement": "i",
        "Problem Resolution": "j"
    }
    for keyword in string_values.split(', '):
        if keyword in value_map:
            final_dict[keyword] = value_map[keyword]
    return final_dict

def map_rating(rating, mapping):
    return mapping.get(rating, '')

def main_start(data):
    rating_mappings = [
        {'Very Good': 'a1', 'Good': 'a2', 'Average': 'a3', 'Poor': 'a4'},
        {'Very Good': 'b1', 'Good': 'b2', 'Average': 'b3', 'Poor': 'b4'},
        {'Very Good': 'c1', 'Good': 'c2', 'Average': 'c3', 'Poor': 'c4'},
        {'Very Good': 'd1', 'Good': 'd2', 'Average': 'd3', 'Poor': 'd4'},
        {'Very Good': 'e1', 'Good': 'e2', 'Average': 'e3', 'Poor': 'e4'},
        {'Very Good': 'f1', 'Good': 'f2', 'Average': 'f3', 'Poor': 'f4'},
        {'Very Good': 'g1', 'Good': 'g2', 'Average': 'g3', 'Poor': 'g4'},
    ]

    for entry in data:
        a = string_1(entry[14])
        b = string_2(entry[15])
        entry_dict = {
            'date': entry[1],
            'company': entry[2],
            'client': entry[3],
            'design': entry[4],
            'phone': entry[5],
            'email': entry[6],
            f'{map_rating(entry[7], rating_mappings[0])}': '✓',
            f'{map_rating(entry[8], rating_mappings[1])}': '✓',
            f'{map_rating(entry[9], rating_mappings[2])}': '✓',
            f'{map_rating(entry[10], rating_mappings[3])}': '✓',
            f'{map_rating(entry[11], rating_mappings[4])}': '✓',
            f'{map_rating(entry[12], rating_mappings[5])}': '✓',
            f'{map_rating(entry[13], rating_mappings[6])}': '✓',
            f'{a.get("Quality")}': '✓',
            f'{a.get("Trust")}': '✓',
            f'{a.get("Brand Name")}': '✓',
            f'{a.get("Previous experience")}': '✓',
            f'{a.get("Word of mouth")}': '✓',
            f'{b.get("Customer Satisfaction")}': '✓',
            f'{b.get("Response Time")}': '✓',
            f'{b.get("Quality of product")}': '✓',
            f'{b.get("Customer Engagement")}': '✓',
            f'{b.get("Problem Resolution")}': '✓',
            'positive_aspects': entry[14],
            'improvement_areas': entry[15],
            'feedback': entry[16],
        }
        doc = DocxTemplate("doc_file_api_files/Spira Power- Feedback Form V2.docx")
        doc.render(entry_dict)
        file_path = "samp_output.docx"
        doc.save(file_path)
