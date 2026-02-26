from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import APIView
class AuthorizationAPIView(APIView):
    def post(self , request):

        # step 1: validation
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # step 2: receive data
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # step 3: authentication
        user = authenticate(username=username, password=password)

        # step 4: return response (if user exists => key else error 401)
        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegistrationAPIView(APIView):
    def post(self, request):
        # step 1: validation
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # step 2: receive data
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # step 3: create user
        user = User.objects.create_user(username=username,
                                        password=password,
                                        is_active=False)
        # create code (6-symbol) -> user
        # step 4: return response
        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id})

