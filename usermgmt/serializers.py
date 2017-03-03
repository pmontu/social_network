from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Customer


class UserSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        use_url=False, required=False,
        source="customer.picture"
    )

    def create(self, validated_data):
        customer = validated_data.pop("customer", None)
        user = User.objects.create_user(**validated_data)

        if customer and customer["picture"]:
            Customer.objects.create(user=user, picture=customer["picture"])

        return user

    class Meta:
        model = User
        fields = (
            "id", "username", "password", "picture",
            "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}


class UserPatchSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        use_url=False, required=False,
        source="customer.picture")

    def update(self, instance, validated_data):
        password = validated_data.get("password", "")
        if password:
            instance.set_password(password)

        customer = validated_data.pop("customer", "")
        if customer:

            picture = customer.pop("picture", "")
            if picture:
                instance.customer.picture.delete()
                instance.customer.picture = picture
                instance.customer.save()

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "id", "username", "password", "picture",
            "first_name", "last_name")
        read_only_fields = ("username", )
        extra_kwargs = {"password": {"required": False, "write_only": True}}