from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins

from utils.mixins import MultiSerializerViewSetMixin
from .serializers import UserSerializer, UserPatchSerializer
from .permissions import AnyoneSignUpOrIsAuthenticated


class UserViewSet(
		MultiSerializerViewSetMixin,
		mixins.UpdateModelMixin,
		mixins.CreateModelMixin,
		mixins.ListModelMixin,
		viewsets.GenericViewSet):
	serializer_class = UserSerializer
	serializer_action_classes = {
		'update': UserPatchSerializer
	}
	queryset = User.objects.filter(is_superuser=False)
	permission_classes = (AnyoneSignUpOrIsAuthenticated, )