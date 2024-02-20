from django.urls import path
from api import views

urlpatterns = [

    path('create_ack',views.Create_AckMail),
    path('read',views.read_Ackmail),
    path('delete',views.delete_Ackmail),
    path('update/<str:pk>',views.update_ackmail),
    path('users_db',views.get_user_db),
    path('import-csv', views.import_csv,),

]