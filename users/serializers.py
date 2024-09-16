from rest_framework import serializers
from .models import Permission, Role, User

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        # fields = ['name']

class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return PermissionSerializer(value).data
    def to_internal_value(self, data):
        return data

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(many=True)

    class Meta:
        model = Role
        fields = ['name', 'permissions']
        
    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permissions.add(*permissions)
        return instance
    
class RoleRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return RoleSerializer(value).data
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)

class UserSerializer(serializers.ModelSerializer):
    role = RoleRelatedField(many=False, queryset=Role.objects.all())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'id', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance