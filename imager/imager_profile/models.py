from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class ActiveManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveManager, self).get_queryset()
        return qs.filter(user__is_active=True)


class ImagerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    region = models.CharField(default='', max_length=255)
    camera = models.CHarField(default='', max_length=255)
    active = ActiveManager()
