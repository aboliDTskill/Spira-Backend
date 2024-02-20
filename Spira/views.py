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
                reporting_to=regstr['reporting_to'] 
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
        email = request.data.get('email')
        password = request.data.get('password')
        user_k = auth.authenticate(email=email, password=password)
        print(user_k)
        if user_k is not None:
            auth.login(request, user_k)
            refresh = RefreshToken.for_user(user_k)
            access_token = str(refresh.access_token)
            user_data = {
                'procurement': user_k.procurement,
                'quote_generator': user_k.quote_generator,
                'user_management': user_k.user_management,
                'quality': user_k.quality,
                'sales_tracker': user_k.sales_tracker
            }
        
            return Response({'output': {'username': email,'accessibilitys': user_data,'access_token': access_token}}, status=status.HTTP_200_OK)
           
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




@api_view(['POST'])        
def update_user(request):
    try:
        username = request.data.get('username')
        user_to_update = User_record.objects.get(user=username)
    except User_record.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        if request.user.role_name == 'Manager':
            updated_data = request.data
            fields_to_update = ['procurement', 'quote_generator', 'user_management', 'quality', 'sales_tracker']# Add more fields as needed
            for field in fields_to_update:
                setattr(user_to_update, field, updated_data.get(field, getattr(user_to_update, field)))

            user_to_update.save()

            return Response({'message': f'User {username} information updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Permission denied. Only Managers can update user information.'}, status=status.HTTP_403_FORBIDDEN)

    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)