from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import AppUser


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        max_length=128, write_only=True,
        style={'input_type': 'password'})

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        AppUser.objects.create(user=user)
        return user

    class Meta:
        model = User