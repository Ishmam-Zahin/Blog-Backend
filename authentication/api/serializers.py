from rest_framework import serializers
from authentication.models import BlogUser

class BlogUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length = 128, write_only = True)
    class Meta:
        model = BlogUser
        exclude = ['is_admin', 'is_active', 'is_staff', 'last_login']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }
    
    def validate(self, data):
        if 'password' in data and 'password2' in data:
            if data['password2'] != data['password']:
                raise serializers.ValidationError({'password2': 'both password must be same'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = BlogUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
            validated_data.pop('password2', None)
        return super().update(instance, validated_data)