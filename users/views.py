# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication, generate_jwt
from .models import Permission, Role, User
from .serializers import RoleSerializer, UserSerializer, PermissionSerializer

@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['confirm_password']:
        raise exceptions.APIException('Passwords do not match')
    
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')
    
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect password')
    response = Response()
    token = generate_jwt(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'message': 'success',
        'jwt': token,
    }
    return response

@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response

class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({
            'data': serializer.data
        })
class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = PermissionSerializer(Permission.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })
        
class RoleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = Role.objects.all()
        serializer = RoleSerializer(queryset, many=True)
        return Response({
            'data': serializer.data
        })
    
    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Role created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        queryset = Role.objects.all()
        role = get_object_or_404(queryset, pk=pk)
        serializer = RoleSerializer(role)
        return Response({
            'data': serializer.data
        })
    
    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Role updated successfully',
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        role.delete()
        return Response({'message': 'Role deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def index(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
