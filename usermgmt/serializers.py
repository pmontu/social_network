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
    picture = serializers.ImageField(
        use_url=False, required=False,
        source="appuser.picture"
    )

    def create(self, validated_data):
        appuser = validated_data.pop("appuser", None)
        user = User.objects.create_user(**validated_data)

        kwargs = {"user": user}
        if appuser:
            kwargs["picture"] = appuser["picture"]
        AppUser.objects.create(**kwargs)
        return user

    class Meta:
        model = User


class UserPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(
        max_length=128, write_only=True,
        style={'input_type': 'password'},
        required=False)
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