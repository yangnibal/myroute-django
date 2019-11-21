from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (action, api_view, permission_classes)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
import random

class PostViewSet(generics.ListAPIView, APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    # 게시글 리스트 반환 제너릭 설정


    def post(self, request):  # 작성자 이름 자동추가 기능을 위해 post용 뷰 분리
        #import pdb;pdb.set_trace()
        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        key = ""
        for i in range(30):
            key += random.choice(possible)
        if request.user.is_authenticated:  # 사용자가 인증 되었을경우
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, postkey=key)  # 작성자 요청자로 설정, 포스트에 키값 부여
                return JsonResponse(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)  # 폼에 오류가 있을 경우
        return Response(status=status.HTTP_401_UNAUTHORIZED)  #인증되지 않았을 경우


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly))
def PostDetail(request, postkey):
    try:
        post = Post.objects.get(postkey=postkey)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)