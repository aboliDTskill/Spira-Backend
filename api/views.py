from django.shortcuts import render
from api.models import AckMail,User_record
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import numpy as np
import pandas as pd
from api.serializers import serialize_ackmails,AckMailSerializer
# Create your views here.
@api_view(['POST'])
def Create_AckMail(request):
    try:
        json_data = json.loads(request.data.get('json_data'))
        email_bdy = request.data.get('email_body')
        attchmnt = request.data.get('attachment')
        qtn_html_body = request.data.get('quotation_html_body')
        qtn_attchmnt = request.data.get('quotation_attachment')
        AckMail.objects.create(
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
            ack_time=json_data['ack_time'])
        return Response('Successfully saved in db',status=status.HTTP_200_OK)
    except json.JSONDecodeError:
        return Response('Invalid JSON format', status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response(f'Missing required field: {str(e)}', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_Ackmail(request):
    try:
        rfrnc_num = request.data.get('refrence_num')
        AckMail.objects.all().delete()
        return Response('Successfully deleted',status=status.HTTP_200_OK)
    except AckMail.DoesNotExist:
        return Response('No Record Found To Delete', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def read_Ackmail(request):
    try:
        ack_mail = AckMail.objects.all()
        serialized_ackmails = serialize_ackmails(ack_mail)
        return Response(serialized_ackmails, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
    
@api_view(['PUT'])
def update_ackmail(request, pk):
    try:
        ackmail = AckMail.objects.get(reference_number=pk)
        serializer = AckMailSerializer(ackmail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Sucessfully', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except AckMail.DoesNotExist:
        return Response('No Record Found To Update', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_users(request):
    
    if request.user.reporting_to == 'All':
        
        users = User_record.objects.all().values()
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to='TeamLeadA').values()
    elif request.user.role_name == 'TeamleadB':
        users = User_record.objects.filter(reporting_to='TeamLeadB').values()
    elif request.user.role_name == 'employee':
        users = User_record.objects.filter(reporting_to = 'employee').values()

    context = {'users': users}
    return Response({'Output':{'users':context}})

@api_view(['GET'])
def get_user_db(request):
    # print(request.user.em)
    if request.user.role_name == 'admin':
        users = User_record.objects.all().values('user')
        user_names = [AckMail.objects.filter(sales_person_name = user['user']).values() for user in users]
    elif request.user.role_name == 'Manager':
        team_leads = User_record.objects.filter(reporting_to=request.user).values('user')
        employee = [User_record.objects.filter(reporting_to=team_members['user']).values('user') for team_members in team_leads]
        for each in employee:
            user_names = [AckMail.objects.filter(sales_person_name = user['user']).values() for user in each]
    elif request.user.role_name == 'Teamlead':
        users = User_record.objects.filter(reporting_to=request.user).values('user')
        user_names = [AckMail.objects.filter(sales_person_name = user['user']).values() for user in users]
    elif request.user.role_name == 'employee':
        user_names = [AckMail.objects.filter(sales_mail = request.user.email).values()]
       
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

            AckMail.objects.create(
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
                ack_time=row['ack_time']
            )
        
        return Response('CSV data imported successfully', status=status.HTTP_200_OK)

    except KeyError as e:
        return Response(f'Missing required field in CSV: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
