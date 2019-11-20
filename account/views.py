from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import (UserSerializer, AuthTokenSerializer)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def token_request(request):
        if user_requested_token() and token_request_is_warranted():
            new_token = Token.objects.create(user=request.user)
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, list=True, methods=['GET'])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, list=True, methods=['POST'])
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(detail=False, list=True, methods=['GET'])
    def logout(self, request):
        if not request.user.is_authenticated:
            print(request.user)
            return Response("Do not exits user")
        request.user.auth_token.delete()
        return Response("user token delete success")