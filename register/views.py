from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


# Create your views here.
class Register(APIView):
    def post(self, request):
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Check if a People or User object with the username or email already exists
            if People.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
                return Response({"message": "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if People.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
                return Response({"message": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a new User instance and link it to People
            user = User.objects.create_user(username=username, email=email, password=password)
            person = serializer.save(user=user)  # Save People record with linked User
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class Login(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if(serializer.is_valid()):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            try:
                person = People.objects.get(username=username)
                
                # Check if People instance has an associated User
                if person.user is None:
                    return Response({"message": "User not linked to People record"}, status=status.HTTP_404_NOT_FOUND)

                # Verify the password against the User instance's password
                if check_password(password, person.user.password):
                    token, created = Token.objects.get_or_create(user=person.user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            except People.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllUser(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        users=People.objects.all()
        serializer=PeopleSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    