from rest_framework import serializers
from .models import AckMail

class AckMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AckMail
        fields = '__all__'


def serialize_ackmails(ackmails):
    serialized_data = []
    for ackmail in ackmails:
        serialized_data.append({
            'reference_number': ackmail.reference_number,
            'sales_mail': ackmail.sales_mail,
            'sales_email_time': ackmail.sales_email_time,
            "client_email" :ackmail.client_email,
            "client_email_time" :ackmail.client_email_time,
            "client_cc" : ackmail.client_cc,
            "client_subject" :ackmail.client_subject,
            "plain_text" : ackmail.plain_text,
            "sales_person_name" :ackmail.sales_person_name,
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
            "email_body":getattr(ackmail,'email_body' ) ,
            "attachment":getattr(ackmail,'attachment' ) ,
            "quotation_html_body":getattr(ackmail,'quotation_html_body' ) ,
            "quotation_attachment":getattr(ackmail,'quotation_attachment' ) ,
            "quotation_attachment":getattr(ackmail,'quotation_attachment' ) ,
            "order_ageing":ackmail.order_ageing,
            "order_date_time":ackmail.order_date_time,
            "order_closure_days":ackmail.order_closure_days,
            "order_value":ackmail.order_value,
            "order_email_attachment":ackmail.order_email_attachment,
        })
    return serialized_data
