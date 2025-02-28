from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'address', 'profile_picture', 'password', 'confirm_password','first_name', 'last_name']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        validated_data['password'] = make_password(validated_data['password']) 
        return super().create(validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture=serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'address', 'profile_picture', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None
    
    def update(self, instance, validated_data):
        if 'profile_picture' in self.context['request'].FILES:
            instance.profile_picture = self.context['request'].FILES['profile_picture']
        return super().update(instance, validated_data)
