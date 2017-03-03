from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
