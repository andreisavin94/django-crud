from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(blank=True, null=True, max_length=11)
    address = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
