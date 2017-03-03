from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import AppUser


class UserSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        use_url=False, required=False,
        source="appuser.picture"
    )

    def create(self, validated_data):
        appuser = validated_data.pop("appuser", None)
        user = User.objects.create_user(**validated_data)

        if appuser and appuser["picture"]:
            AppUser.objects.create(user=user, picture=appuser["picture"])

        return user

    class Meta:
        model = User
        fields = ("id", "username", "password", "picture")
        extra_kwargs = {"password": {"write_only": True}}


class UserPatchSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        use_url=False, required=False,
        source="appuser.picture")

    def update(self, instance, validated_data):
        password = validated_data.get("password", "")
        if password:
            instance.set_password(password)

        appuser = validated_data.pop("appuser", "")
        if appuser:
            picture = appuser.pop("picture", "")
            instance.appuser.picture = picture
            instance.appuser.save()

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "username", "password", "picture")
        read_only_fields = ("username", )
        extra_kwargs = {"password": {"required": False, "write_only": True}}