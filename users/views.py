# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from testdrive.pagination import CustomPageNumberPagination
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
        data = UserSerializer(user).data
        data['permissions'] = [p['name'] for p in data.role.permissions.values()]
        return Response({
            'data': data
        })
class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
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
    

class UserGenericApiView(
    generics.GenericAPIView, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    
    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data            
            })

        return self.list(request)
        
    def post(self, request):
        request.data.update({
            'password': 123,
            'role': request.data['role_id']
        })
        return Response({
            'message': 'User created successfully',
            'data': self.create(request).data
        }, status=status.HTTP_201_CREATED)
        
    def put(self, request, pk=None):
        if 'role_id' in request.data:
            request.data.update({
                'role': request.data['role_id']
            })
        return Response({
            'message': 'User updated',
            'data': self.partial_update(request, pk).data
        })
    
    def delete(self, request, pk=None):
        self.destroy(request, pk)
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class ProfileInfoApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        # return Response({
        #     'message': 'User updated successfully',
        #     'data': serializer.data
        # })
        
class ProfilePasswordApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk=None):
        user = request.user
        data = request.data
        if data['password'] != data['confirm_password']:
            raise exceptions.APIException('Passwords do not match')
        
        user.set_password(data['password'])
        user.save()
        return Response({
            'message': 'Password updated successfully'
        })