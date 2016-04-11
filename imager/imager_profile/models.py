from django.db import models
from django.contrib.auth.models import User


class ActiveManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveManager, self).get_queryset()
        return qs.filter(user__is_active=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, default='username')
    email = models.EmailField(default='email')
    region = models.CharField(default='region')
    camera = models.CHarField(default='camera')
