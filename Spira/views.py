from api.models import User_record
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.contrib import auth

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    try:
        regstr = request.data
        if User_record.objects.filter(user=regstr['username']).exists():
            return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)
        else:
            User_record.objects.create(
                user=regstr['username'],
                password=regstr['password'],
                email=regstr['email'],
                role_name=regstr['role_name'],
                control = regstr['control']
            )
            return Response('Successfully saved in DB', status=status.HTTP_201_CREATED)
    except json.JSONDecodeError:
        return Response('Invalid JSON format', status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response(f'Missing required field: {str(e)}', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    try:
        user_profiles = User_record.objects.all()
        username = request.data.get('username')
        password = request.data.get('password')
        user_k = auth.authenticate(username=username, password=password)

        if user_k is not None:
            auth.login(request, user_k)
            refresh = RefreshToken.for_user(user_k)
            access_token = str(refresh.access_token)
            # if request.user.control == 'All':
            #     print(request.user.control)
            #     users = User_record.objects.all().values()
            # elif request.user.role_name == 'TeamleadA':
            #     users = User_record.objects.filter(control='TeamLeadA').values()
            # elif request.user.role_name == 'TeamleadB':
            #     users = User_record.objects.filter(control='TeamLeadB').values()
            # elif request.user.role_name == 'employee':
            #     users = User_record.objects.filter(control = 'employee').values()

            # context = {'users': users}
        
            return Response({'output': {'username': username,'access_token': access_token}}, status=status.HTTP_200_OK)
           
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def delete_users(request):
    user_name = request.data.get('username')
    User_record.objects.get(user = user_name).delete()
    return Response('Sucessfully deleted')

        

