from django.urls import path
from api import views

urlpatterns = [

    path('create_ack',views.Create_AckMail),#
    path('read',views.read_Ackmail),#
    path('delete',views.delete_Ackmail),
    path('update/<str:pk>',views.update_ackmail),
    path('get_users',views.get_users),
    path('users_db',views.get_user_db),
    path('import-csv', views.import_csv,),#
    path('waiting_quote',views.get_waiting_quote_record),
    path('waiting_order',views.get_waiting_order_record),
    path('order_place',views.get_order_placed_record),
    path('customer_feedback',views.feedback_data),#filling feedback data and storing the binary form of it 
    path('get_feedback_data', views.get_feedback_data),#fetching the feeedback
    path('download_docx/<int:feedback_id>', views.download_docx, name='download_docx'),
    path('price_list', views.get_price_list),
    path('quote_file', views.get_quote_list),
    path('upload_pdf', views.upload_pdf),
    
    
    

]
