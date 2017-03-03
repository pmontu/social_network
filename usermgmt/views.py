from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins

from .serializers import UserSerializer
from .permissions import AnyoneSignUpOrIsAuthenticated


class UserViewSet(
		mixins.CreateModelMixin,
		mixins.ListModelMixin,
		viewsets.GenericViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.filter(is_superuser=False)
	permission_classes = (AnyoneSignUpOrIsAuthenticated, )