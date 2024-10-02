from rest_framework import serializers
from .models import ack_mail  



class AckMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ack_mail
        fields = '__all__'



def serialize_ackmails(ackmails):
    serialized_data = []
    for ackmail in ackmails:
        serialized_data.append({
            'reference_number': ackmail.reference_number,
            'sales_mail': ackmail.sales_mail,
            'sales_email_time': ackmail.sales_email_time,
            "client_email" : ackmail.client_email,
            "client_email_time" : ackmail.client_email_time,
            "client_cc" : ackmail.client_cc,
            "client_subject" : ackmail.client_subject,
            "plain_text" : ackmail.plain_text,
            "sales_person_name" : ackmail.sales_person_name,
            "client_person_name" : ackmail.client_person_name,
            "quotation_time" : ackmail.quotation_time,
            "quotation_to" : ackmail.quotation_to,
            "quotation_from" : ackmail.quotation_from,
            "quotation_subject" : ackmail.quotation_subject,
            "quotation_plain_body" : ackmail.quotation_plain_body,
            "total_order_value" : ackmail.total_order_value,
            "currency" : ackmail.currency,
            "currency_value" : ackmail.currency_value,
            "reminder_status" : ackmail.reminder_status,
            "ack_time" : ackmail.ack_time,
            "email_body": ackmail.email_body if ackmail.email_body else None,
            "attachment": ackmail.attachment if ackmail.attachment else None,
            "quotation_html_body": ackmail.quotation_html_body if ackmail.quotation_html_body else None,
            "quotation_attachment": ackmail.quotation_attachment if ackmail.quotation_attachment else None,
        })
    return serialized_data



from rest_framework import serializers
from .models import CustomerFeedback

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'