from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import Http404
from django.contrib.auth import authenticate
from authentication.api.serializers import BlogUserSerializer
from authentication.models import BlogUser

@api_view(['GET'])
def user_info(request):
    if request.user.is_authenticated:
        serializer = BlogUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data={}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_user_logout(request):
    request.user.auth_token.delete()
    return Response({'detail': 'logout successfull'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def blog_user_login(request):
    user = authenticate(email = request.data['email'], password = request.data['password'])
    if user is not None:
        token, created = Token.objects.get_or_create(user = user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response(data={'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class BlogUserList(APIView):
    def get(self, request):
        users = BlogUser.objects.all()
        serializer = BlogUserSerializer(users, many = True)
        return Response(data=serializer.data)
    
    def post(self, request):
        serializer = BlogUserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = BlogUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogUserDetails(APIView):
    def get_user(self, id):
        try:
            user = BlogUser.objects.get(id = id)
        except:
            raise Http404
        
        return user
    
    def get(self, request, id):
        user = self.get_user(id)
        serializer = BlogUserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        user = self.get_user(id)
        serializer = BlogUserSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            user = serializer.save()
            serializer = BlogUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)