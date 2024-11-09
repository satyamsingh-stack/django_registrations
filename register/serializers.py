from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model=People
        fields='__all__'
    
    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = make_password(password)
        return super().create(validated_data)
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()