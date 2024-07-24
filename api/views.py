from django.shortcuts import render
from api.models import User_record, ack_mail, CustomerFeedback
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import numpy as np
import pandas as pd
from api.serializers import serialize_ackmails,AckMailSerializer
from django.http import JsonResponse
from datetime import datetime
import json
import base64
# Create your views here.
@api_view(['POST'])
def Create_AckMail(request):
    try:
        json_data = json.loads(request.data.get('json_data'))
        email_bdy = request.data.get('email_body')
        attchmnt = request.data.get('attachment')
        qtn_html_body = request.data.get('quotation_html_body')
        qtn_attchmnt = request.data.get('quotation_attachment')
        ack_mail.objects.create(
            reference_number=json_data['reference_number'],
            sales_mail=json_data['sales_mail'],
            sales_email_time=json_data['sales_email_time'],
            client_email=json_data['client_email'],
            client_email_time=json_data['client_email_time'],
            client_cc=json_data['client_cc'],
            client_subject=json_data['client_subject'],
            email_body=email_bdy,
            attachment=attchmnt,
            plain_text=json_data['plain_text'],
            sales_person_name=json_data['sales_person_name'],
            client_person_name=json_data['client_person_name'],
            quotation_time=json_data['quotation_time'],
            quotation_to=json_data['quotation_to'],
            quotation_from=json_data['quotation_from'],
            quotation_subject=json_data['quotation_subject'],
            quotation_plain_body=json_data['quotation_plain_body'],
            quotation_html_body=qtn_html_body,
            quotation_attachment=qtn_attchmnt,
            total_order_value=json_data['total_order_value'],
            currency=json_data['currency'],
            currency_value=json_data['currency_value'],
            reminder_status=json_data['reminder_status'],
            ack_time=json_data['ack_time'],
            order_ageing=json_data['order_ageing'],
            order_date_time=json_data['order_date_time'],
            order_closure_days =json_data['order_closure_days'],
            order_value=json_data['order_value'],
            order_email_attachment=json_data['order_email_attachment'])
        
        return Response('Successfully saved in db',status=status.HTTP_200_OK)
    except json.JSONDecodeError:
        return Response('Invalid JSON format', status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response(f'Missing required field: {str(e)}', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_Ackmail(request):
    try:
        sales_mail = request.data.get('sales_mail')
        rfrnc_num = request.data.get('rfrnc_num')
        ack_mail_obj = ack_mail.objects.get(sales_mail=sales_mail, reference_number=rfrnc_num)
        ack_mail_obj.delete()
        return Response('Successfully deleted',status=status.HTTP_200_OK)
    except ack_mail.DoesNotExist:
        return Response('No Record Found To Delete', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def read_Ackmail(request):
    try:
        ack_maill = ack_mail.objects.all()
        serialized_ackmails = serialize_ackmails(ack_maill)
        return Response(serialized_ackmails, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
    
@api_view(['PUT'])
def update_ackmail(request, pk):
    try:
        email = request.data.get("email")
        jsondata_str = request.data.get("jsondata")

        # Convert jsondata_str to dictionary
        data_dict = json.loads(jsondata_str) if jsondata_str else {}

        if not data_dict:
            return Response("No data provided for update", status=status.HTTP_400_BAD_REQUEST)

        ackmail_query = ack_mail.objects.filter(reference_number=pk, sales_mail=email)

        if ackmail_query.exists():
            allowed_roles = ['admin', 'Manager', 'Teamlead']
            if request.user.role_name in allowed_roles:
                columns = {key: value for key, value in data_dict.items()}
                ack_mail.objects.filter(reference_number=pk, sales_mail=email).update(**columns) 
                return Response('Updated Successfully', status=status.HTTP_200_OK)
            else:
                return Response('Permission denied. Only Managers, Team Leads, and Admins can update AckMail.', status=status.HTTP_403_FORBIDDEN)

        else:
            return Response('No Record Found To Update', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_users(request):
    
    if request.user.role_name == 'admin':
        users = User_record.objects.all().values('created_date','last_login','user','email','role_name','reporting_to','sales_tracker','user_management','quality','procurement','quote_generator')
    elif request.user.role_name == 'Manager':
        users = []
        teamleads = User_record.objects.filter(reporting_to=request.user).values('created_date','last_login','user','email','role_name','reporting_to','sales_tracker','user_management','quality','procurement','quote_generator')
        users.append(teamleads)
        employee = [User_record.objects.filter(reporting_to=team_members['user']).values('created_date','last_login','user','email','role_name','reporting_to','sales_tracker','user_management','quality','procurement','quote_generator') for team_members in User_record.objects.filter(reporting_to=request.user).values('user')]
        users.append(employee)
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to=request.user).values()
    return Response({'Output':{'record':users,'Role':request.user.role_name,"Name":request.user.user}})


@api_view(['GET'])
def get_user_db(request):
    if request.user.role_name == 'admin':
        users = User_record.objects.all().values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user']).values( 'reminder_status','reference_number','sales_person_name','sales_mail','sales_email_time','client_person_name','client_email','client_email_time','client_cc','client_subject','ack_time','quotation_time') for user in users]
    elif request.user.role_name == 'Manager':
        user_names=[]
        team_leads = User_record.objects.filter(reporting_to=request.user).values('user')
        employee = [User_record.objects.filter(reporting_to=team_members['user']).values('user') for team_members in team_leads]
        for each in employee:
            record = [ack_mail.objects.filter(sales_person_name = user['user']).values( 'reminder_status','reference_number','sales_person_name','sales_mail','sales_email_time','client_person_name','client_email','client_email_time','client_cc','client_subject','ack_time','quotation_time') for user in each]
            user_names.append(record)
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to=request.user).values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user']).values( 'reminder_status','reference_number','sales_person_name','sales_mail','sales_email_time','client_person_name','client_email','client_email_time','client_cc','client_subject','ack_time','quotation_time') for user in users]
    elif request.user.role_name == 'employee':
        user_names = [ack_mail.objects.filter(sales_mail = request.user.email).values( 'reminder_status','reference_number','sales_person_name','sales_mail','sales_email_time','client_person_name','client_email','client_email_time','client_cc','client_subject','ack_time','quotation_time')]
       
    return Response(user_names)
    
  

@api_view(['POST'])
def import_csv(request):
    try:
        csv_file = request.FILES['csv_file']
        
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            currency_value = row['currency_value']
            if pd.notna(currency_value) and np.isnan(currency_value):
                currency_value = None

            ack_mail.objects.create(
                reference_number=row['reference_number'],
                sales_mail=row['sales_mail'],
                sales_email_time=row['sales_email_time'],
                client_email=row['client_email'],
                client_email_time=row['client_email_time'],
                client_cc=row['client_cc'],
                client_subject=row['client_subject'],
                #email_body=row['email_body'] if not pd.isnull(row['email_body']) else None,
                #attachment=row['attachment'] if not pd.isnull(row['attachment']) else None,
                plain_text=row['plain_text'] if not pd.isnull(row['plain_text']) else None,
                sales_person_name=row['sales_person_name'] if not pd.isnull(row['sales_person_name']) else None,
                client_person_name=row['client_person_name'] if not pd.isnull(row['client_person_name']) else None,
                quotation_time=row['quotation_time'],
                quotation_to=row['quotation_to'],
                quotation_from=row['quotation_from'],
                quotation_subject=row['quotation_subject'],
                quotation_plain_body=row['quotation_plain_body'],
                #quotation_html_body=row['quotation_html_body'],
                #quotation_attachment=row['quotation_attachment'],
                total_order_value=row['total_order_value'],
                currency=row['currency'],
                currency_value=currency_value,
                reminder_status=row['reminder_status'],
                ack_time=row['ack_time'],
                order_ageing =row['order_ageing'],
                order_date_time=row['order_date_time'],
                order_closure_days=row['order_closure_days'],
                order_value=row['order_value'],
                order_email_attachment=row['order_email_attachment'],
            )
        
        return Response('CSV data imported successfully', status=status.HTTP_200_OK)

    except KeyError as e:
        return Response(f'Missing required field in CSV: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_waiting_quote_record(request):
    if request.user.role_name == 'admin':
        users = User_record.objects.all().values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='pending').values('sales_mail','client_cc','ack_time','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','sales_email_time') for user in users]
    elif request.user.role_name == 'Manager':
        user_names=[]
        team_leads = User_record.objects.filter(reporting_to=request.user).values('user')
        employee = [User_record.objects.filter(reporting_to=team_members['user']).values('user') for team_members in team_leads]
        for each in employee:
            record = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='pending').values( 'sales_mail','client_cc','ack_time','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','sales_email_time') for user in each]
            user_names.append(record)
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to=request.user).values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='pending').values( 'sales_mail','client_cc','ack_time','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','sales_email_time') for user in users]
    elif request.user.role_name == 'employee':
        user_names = [ack_mail.objects.filter(sales_mail = request.user.email,reminder_status='pending').values( 'sales_mail','client_cc','ack_time','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','sales_email_time')]
    return Response(user_names)


@api_view(['GET'])
def get_waiting_order_record(request):
    if request.user.role_name == 'admin':
        users = User_record.objects.all().values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='success').values('sales_mail', 'client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','quotation_time') for user in users]
    elif request.user.role_name == 'Manager':
        user_names=[]
        team_leads = User_record.objects.filter(reporting_to=request.user).values('user')
        employee = [User_record.objects.filter(reporting_to=team_members['user']).values('user') for team_members in team_leads]
        for each in employee:
            record = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='success').values( 'sales_mail','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','quotation_time') for user in each]
            user_names.append(record)
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to=request.user).values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='success').values( 'sales_mail','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','quotation_time') for user in users]
    elif request.user.role_name == 'employee':
        user_names = [ack_mail.objects.filter(sales_mail = request.user.email,reminder_status='success').values( 'sales_mail','client_email','reference_number','sales_person_name','reminder_status','order_ageing','client_person_name','client_subject','client_email_time','quotation_time')]
    return Response(user_names)

@api_view(['GET'])
def get_order_placed_record(request):
    if request.user.role_name == 'admin':
        users = User_record.objects.all().values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='order_placed').values('client_email','reference_number','sales_person_name','reminder_status','order_value','order_date_time') for user in users]
    elif request.user.role_name == 'Manager':
        user_names=[]
        team_leads = User_record.objects.filter(reporting_to=request.user).values('user')
        employee = [User_record.objects.filter(reporting_to=team_members['user']).values('user') for team_members in team_leads]
        for each in employee:
            record = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='order_placed').values('client_email','reference_number','sales_person_name','reminder_status','order_value','order_date_time') for user in each]
            user_names.append(record)
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to=request.user).values('user')
        user_names = [ack_mail.objects.filter(sales_person_name = user['user'],reminder_status='order_placed').values('client_email','reference_number','sales_person_name','reminder_status','order_value','order_date_time') for user in users]
    elif request.user.role_name == 'employee':
        user_names = [ack_mail.objects.filter(sales_mail = request.user.email,reminder_status='order_placed').values('client_email','reference_number','sales_person_name','reminder_status','order_value','order_date_time')]
    return Response(user_names)

########################################### FEEDBACK  API ####################################################

from files.email_feedback import main
@api_view(['POST'])
def feedback_data(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Create a dictionary with all feedback fields
        feedback_dict = {
            'about_team_product_service': ', '.join(data.get('about_team_product_service', [])),
            'client_disignation': data.get('client_disignation'),
            'client_name': data.get('client_name'),
            'company_name': data.get('company_name'),
            'customer_statisfaction_rate': data.get('customer_statisfaction_rate'),
            'email_address': data.get('email_address'),
            'form_date': datetime.now().date().strftime("%m/%d/%Y"),
            'form_timestamp': datetime.now().replace(microsecond=0).isoformat(),
            'other_feedback': data.get('other_feedback'),
            'product_quality_punctuality_rate': data.get('product_quality_punctuality_rate'),
            'quality_rate': data.get('quality_rate'),
            'service_provider_rate': ', '.join(data.get('service_provider_rate', [])),
            'services_experience_rate': data.get('services_experience_rate'),
            'team_communication_rate': data.get('team_communication_rate'),
            'team_help_rate': data.get('team_help_rate'),
            'technical_enquires_rate': data.get('technical_enquires_rate'),
            'telephone_number': data.get('telephone_number')
        }

        # Serialize the dictionary to a JSON string
        
        feedback_json = json.dumps(feedback_dict, ensure_ascii=False)
        print(feedback_json)
        # Encode the JSON string to bytes and then to base64
        feedback_bytes = feedback_json.encode('utf-8')
        
        print(feedback_bytes)
        email_screenshot_base64 = base64.b64encode(feedback_bytes)
        
        # Create and save the CustomerFeedback instance
        feedback = CustomerFeedback(
            form_timestamp=feedback_dict['form_timestamp'],
            form_date=feedback_dict['form_date'],
            company_name=feedback_dict['company_name'],
            client_name=feedback_dict['client_name'],
            client_disignation=feedback_dict['client_disignation'],
            telephone_number=feedback_dict['telephone_number'],
            email_address=feedback_dict['email_address'],
            quality_rate=feedback_dict['quality_rate'],
            services_experience_rate=feedback_dict['services_experience_rate'],
            technical_enquires_rate=feedback_dict['technical_enquires_rate'],
            team_communication_rate=feedback_dict['team_communication_rate'],
            team_help_rate=feedback_dict['team_help_rate'],
            product_quality_punctuality_rate=feedback_dict['product_quality_punctuality_rate'],
            customer_statisfaction_rate=feedback_dict['customer_statisfaction_rate'],
            service_provider_rate=feedback_dict['service_provider_rate'],
            about_team_product_service=feedback_dict['about_team_product_service'],
            other_feedback=feedback_dict['other_feedback'],
            email_screenshot=email_screenshot_base64  # Save base64 encoded data
        )
        
        feedback.save()
        
        print(feedback_dict['email_address'])
        main(feedback_dict['email_address'])
        return Response({"message": "Data inserted successfully"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)



# @api_view(['POST'])
# def feedback_data(request):
#     try:
#         data = json.loads(request.body)
#         about_team_product_service = ', '.join(data.get('about_team_product_service', []))
#         client_disignation = data.get('client_disignation')
#         client_name = data.get('client_name')
#         company_name = data.get('company_name')
#         customer_statisfaction_rate = data.get('customer_statisfaction_rate')
#         email_address = data.get('email_address')
#         current_date = datetime.now().date()
#         formatted_current_date = current_date.strftime("%m/%d/%Y")
#         form_date = formatted_current_date
#         current_date_and_time = datetime.now().replace(microsecond=0)
#         form_timestamp = current_date_and_time
#         other_feedback = data.get('other_feedback')
#         product_quality_punctuality_rate = data.get('product_quality_punctuality_rate')
#         quality_rate = data.get('quality_rate')
#         service_provider_rate = ', '.join(data.get('service_provider_rate', []))
#         services_experience_rate = data.get('services_experience_rate')
#         team_communication_rate = data.get('team_communication_rate')
#         team_help_rate = data.get('team_help_rate')
#         technical_enquires_rate = data.get('technical_enquires_rate')
#         telephone_number = data.get('telephone_number')

#         feedback = CustomerFeedback(
#             form_timestamp=form_timestamp,
#             form_date=form_date,
#             company_name=company_name,
#             client_name=client_name,
#             client_disignation=client_disignation,
#             telephone_number=telephone_number,
#             email_address=email_address,
#             quality_rate=quality_rate,
#             services_experience_rate=services_experience_rate,
#             technical_enquires_rate=technical_enquires_rate,
#             team_communication_rate=team_communication_rate,
#             team_help_rate=team_help_rate,
#             product_quality_punctuality_rate=product_quality_punctuality_rate,
#             customer_statisfaction_rate=customer_statisfaction_rate,
#             service_provider_rate=service_provider_rate,
#             about_team_product_service=about_team_product_service,
#             other_feedback=other_feedback
#         )
#         feedback.save()
#         main(email_address)
#         return Response({"message": "Data inserted successfully"}, status=201)
#     except Exception as e:
#         return Response({"error": str(e)}, status=400)
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse, HttpResponse
# from django.utils.timezone import now
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from api.models import CustomerFeedback
# import json
# import os
# from io import BytesIO
# from datetime import datetime

# @api_view(['POST'])
# def feedback_data(request):
#     try:
#         data = json.loads(request.body)
#         about_team_product_service = ', '.join(data.get('about_team_product_service', []))
#         client_disignation = data.get('client_disignation')
#         client_name = data.get('client_name')
#         company_name = data.get('company_name')
#         customer_statisfaction_rate = data.get('customer_statisfaction_rate')
#         email_address = data.get('email_address')
#         current_date = datetime.now().date()
#         formatted_current_date = current_date.strftime("%m/%d/%Y")
#         form_date = formatted_current_date
#         current_date_and_time = datetime.now().replace(microsecond=0)
#         form_timestamp = current_date_and_time
#         other_feedback = data.get('other_feedback')
#         product_quality_punctuality_rate = data.get('product_quality_punctuality_rate')
#         quality_rate = data.get('quality_rate')
#         service_provider_rate = ', '.join(data.get('service_provider_rate', []))
#         services_experience_rate = data.get('services_experience_rate')
#         team_communication_rate = data.get('team_communication_rate')
#         team_help_rate = data.get('team_help_rate')
#         technical_enquires_rate = data.get('technical_enquires_rate')
#         telephone_number = data.get('telephone_number')

#         feedback = CustomerFeedback(
#             form_timestamp=form_timestamp,
#             form_date=form_date,
#             company_name=company_name,
#             client_name=client_name,
#             client_disignation=client_disignation,
#             telephone_number=telephone_number,
#             email_address=email_address,
#             quality_rate=quality_rate,
#             services_experience_rate=services_experience_rate,
#             technical_enquires_rate=technical_enquires_rate,
#             team_communication_rate=team_communication_rate,
#             team_help_rate=team_help_rate,
#             product_quality_punctuality_rate=product_quality_punctuality_rate,
#             customer_statisfaction_rate=customer_statisfaction_rate,
#             service_provider_rate=service_provider_rate,
#             about_team_product_service=about_team_product_service,
#             other_feedback=other_feedback
#         )
#         feedback.save()
#         main(email_address)
        
#         # Generate PDF
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer, pagesize=letter)
#         p.drawString(100, 750, f"Feedback Form")
#         p.drawString(100, 730, f"Date: {form_date}")
#         p.drawString(100, 710, f"Client Name: {client_name}")
#         p.drawString(100, 690, f"Client Disignation: {client_disignation}")
#         p.drawString(100, 670, f"Company Name: {company_name}")
#         p.drawString(100, 650, f"Email Address: {email_address}")
#         p.drawString(100, 630, f"Telephone Number: {telephone_number}")
#         p.drawString(100, 610, f"Quality Rate: {quality_rate}")
#         p.drawString(100, 590, f"Services Experience Rate: {services_experience_rate}")
#         p.drawString(100, 570, f"Technical Enquires Rate: {technical_enquires_rate}")
#         p.drawString(100, 550, f"Team Communication Rate: {team_communication_rate}")
#         p.drawString(100, 530, f"Team Help Rate: {team_help_rate}")
#         p.drawString(100, 510, f"Product Quality Punctuality Rate: {product_quality_punctuality_rate}")
#         p.drawString(100, 490, f"Customer Statisfaction Rate: {customer_statisfaction_rate}")
#         p.drawString(100, 470, f"Service Provider Rate: {service_provider_rate}")
#         p.drawString(100, 450, f"About Team/Product/Service: {about_team_product_service}")
#         p.drawString(100, 430, f"Other Feedback: {other_feedback}")

#         p.showPage()
#         p.save()

#         buffer.seek(0)

#         # Create response to download the PDF
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="feedback.pdf"'
#         return response

#     except Exception as e:
#         return Response({"error": str(e)}, status=400)

#################################### FETCHING THE FEEDBACK DATA AND RETURNING AS RESPONSE #################################



# @api_view(['GET'])
# def get_feedback_data(request):
#     try:
#         feedback_id = request.data.get('id')  # Use query_params for GET requests
#         if not feedback_id:
#             return Response({"error": "Feedback ID is required"}, status=400)
        
#         feedback = get_object_or_404(CustomerFeedback, pk=feedback_id)
        
#         if not feedback.email_screenshot:
#             return Response({"error": "No screenshot data available"}, status=400)
        
#         try:
#             email_screenshot_bytes = base64.b64decode(feedback.email_screenshot)
#         except (base64.binascii.Error, ValueError):
#             return Response({"error": "Base64 decoding failed"}, status=400)
        
#         try:
#             feedback_json = email_screenshot_bytes.decode('utf-8')
#             if not feedback_json:
#                 return Response({"error": "Decoded JSON string is empty"}, status=400)
#             feedback_dict = json.loads(feedback_json)
#         except json.JSONDecodeError:
#             return Response({"error": "JSON decoding failed"}, status=400)
        
#         return Response({"feedback_data": feedback_dict}, status=200)
    
#     except CustomerFeedback.DoesNotExist:
#         return Response({"error": "Feedback not found"}, status=404)
#     except Exception as e:
#         return Response({"error": str(e)}, status=400)

import base64
import json
import pdfkit
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomerFeedback
@api_view(['GET'])
def get_feedback_data(request):
    try:
        feedback_id = request.data.get('id')  # Use query_params for GET requests
        if not feedback_id:
            return Response({"error": "Feedback ID is required"}, status=400)
        
        feedback = get_object_or_404(CustomerFeedback, pk=feedback_id)
        
        if not feedback.email_screenshot:
            return Response({"error": "No screenshot data available"}, status=400)
        
        try:
            email_screenshot_bytes = base64.b64decode(feedback.email_screenshot)
        except (base64.binascii.Error, ValueError):
            return Response({"error": "Base64 decoding failed"}, status=400)
        
        try:
            feedback_json = email_screenshot_bytes.decode('utf-8')
            if not feedback_json:
                return Response({"error": "Decoded JSON string is empty"}, status=400)
            feedback_dict = json.loads(feedback_json)
        except json.JSONDecodeError:
            return Response({"error": "JSON decoding failed"}, status=400)
        
        # Convert feedback_dict to HTML
        html_content = "<html><body>"
        for key, value in feedback_dict.items():
            html_content += f"<p><strong>{key}:</strong> {value}</p>"
        html_content += "</body></html>"
        
        # Generate PDF from HTML
        pdf = pdfkit.from_string(html_content, False)
        
        # Return PDF as a response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="feedback.pdf"'
        return response
    
    except CustomerFeedback.DoesNotExist:
        return Response({"error": "Feedback not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)




    

#################################download docx##########################################
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from io import BytesIO
import json
import docx2pdf
import pythoncom
from .models import CustomerFeedback
from doc_file_api_files import doc_templete_create_v1  # Ensure this is in the same directory or adjust the import path

def doc_file(sample_data):
    print(sample_data)
    doc_templete_create_v1.main_start(sample_data)

    input_file = "samp_output.docx"
    output_file = "samp_pdf_output.pdf"
    pythoncom.CoInitialize()
    docx2pdf.convert(input_file, output_file)

    docx_file_path = "samp_pdf_output.pdf"

    with open(docx_file_path, 'rb') as file:
        pdf_data = file.read()

    pdf_bytes = bytes(pdf_data)
    return pdf_bytes

@api_view(["GET"])
def download_docx(request, feedback_id):
    try:
        feedback = get_object_or_404(CustomerFeedback, pk=feedback_id)
        
        if feedback.doc_file is None:
            print("hwllo+++++++++++++++++++++++")
            sample_data = [
                feedback.form_timestamp,
                feedback.form_date,
                feedback.company_name,
                feedback.client_name,
                feedback.client_disignation,
                feedback.telephone_number,
                feedback.email_address,
                feedback.quality_rate,
                feedback.services_experience_rate,
                feedback.technical_enquires_rate,
                feedback.team_communication_rate,
                feedback.team_help_rate,
                feedback.product_quality_punctuality_rate,
                feedback.customer_statisfaction_rate,
                feedback.service_provider_rate,
                feedback.about_team_product_service,
                feedback.other_feedback
            ]
            doc_data = doc_file([sample_data])
            feedback.doc_file = doc_data
            feedback.save()
        else:
            doc_data = feedback.doc_file

        # Create a BytesIO object to send the file as attachment
        file_obj = BytesIO()
        file_obj.write(doc_data)
        file_obj.seek(0)

        # Set the response headers for attachment download
        response = HttpResponse(file_obj, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=downloaded_doc.pdf'
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

##########################################################################

from .models import PriceListV2




@api_view(["POST"])
def get_price_list(request):
    try:
        data = request.data
        item = data.get('item')
        winding_material = data.get('winding_material')
        filler_material = data.get('filler_material')
        inner_ring_material = data.get('inner_ring_material')
        outer_ring_material = data.get('outer_ring_material')
        material_size = data.get('material_size')
        rating = data.get('rating')

        # Query the database using Django ORM
        prices = PriceListV2.objects.filter(
            item=item,
            winding_material=winding_material,
            filler_material=filler_material,
            inner_ring_material=inner_ring_material,
            outer_ring_material=outer_ring_material,
            material_size=material_size,
            rating=rating
        ).values('price')

        # Convert the QuerySet to a list
        price_list = list(prices)

        return JsonResponse(price_list, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
###########WITH EXCEPTION HANDLING######################
# @api_view(["POST"])
# def get_price_list(request):
#     try:
#         data = request.data
#         item = data.get('item')
#         winding_material = data.get('winding_material')
#         filler_material = data.get('filler_material')
#         inner_ring_material = data.get('inner_ring_material')
#         outer_ring_material = data.get('outer_ring_material')
#         material_size = data.get('material_size')
#         rating = data.get('rating')

#         # Validate that all required parameters are provided
#         if not all([item, winding_material, filler_material, inner_ring_material, outer_ring_material, material_size, rating]):
#             raise ValueError("All parameters must be provided")

#         # Query the database using Django ORM
#         prices = PriceListV2.objects.filter(
#             item=item,
#             winding_material=winding_material,
#             filler_material=filler_material,
#             inner_ring_material=inner_ring_material,
#             outer_ring_material=outer_ring_material,
#             material_size=material_size,
#             rating=rating
#         ).values('price')

#         # Convert the QuerySet to a list
#         price_list = list(prices)

#         if not price_list:
#             raise ObjectDoesNotExist("No matching prices found")

#         return JsonResponse(price_list, safe=False)

#     except ValueError as ve:
#         return JsonResponse({"error": str(ve)}, status=400)
#     except ObjectDoesNotExist as odne:
#         return JsonResponse({"error": str(odne)}, status=404)
#     except ValidationError as ve:
#         return JsonResponse({"error": "Invalid data provided"}, status=400)
#     except OperationalError as oe:
#         return JsonResponse({"error": "Database connection error"}, status=500)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

from docxtpl import DocxTemplate

@api_view(["POST"])
def get_quote_list(request):
    try:
        data = request.data
        doc_template_path = "Quote_v1.docx"
        doc_output_path = "quote_output_1.docx"

        # Render the template with the provided data
        doc = DocxTemplate(doc_template_path)
        doc.render(data)

        # Save the rendered document
        doc.save(doc_output_path)

        # Path to the converted PDF file
        pdf_output_path = "spira_backend/quote_pdf_output.pdf"

        # Optionally, convert the DOCX to PDF using external tool like LibreOffice or other converter

        # Send the converted file as response
        with open(pdf_output_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="quote_pdf_output.pdf"'
            return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pdfupload import pdf_to_img

import os

@api_view(["POST"])
def upload_pdf(request):
    try:
        # Check if a PDF file is present in the request
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file part'}, status=400)
        
        file = request.FILES['file']
        print(file.name+"44444444444444444444444444444444444")
        # Check if the file is a PDF
        if file.name == '':
            return JsonResponse({'error': 'No selected file'}, status=400)

        if file and file.name.endswith('.pdf'):
            # Save the file to the uploads folder
            path = os.path.join("pdf_files", 'pdf_extraction.pdf')
            default_storage.save(path, ContentFile(file.read()))
        
            print("dsffffffffffffffffffffffffffffffffffffffff")
            main_output_folder = "output_image"
            texts_to_detect = ["Chemical Composition (%)", 'Mechanical Properties']
            print(path)
            pdf_to_img.crop_pdf_pages_with_text(path, main_output_folder, texts_to_detect)
            pdf_to_img.fetch_jpeg_images(main_output_folder)

            return JsonResponse({'message': 'File uploaded successfully', 'filename': path})
        else:
            return JsonResponse({'error': 'Invalid file format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)