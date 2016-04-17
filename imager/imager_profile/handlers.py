# -*- coding: utf-8 -*-
"""signal handlers registered by the imager_profile app"""
from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ImagerProfile
import logging


logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_imager_profile(sender, **kwargs):
    if kwargs.get('created', False):
        try:
            new_profile = ImagerProfile(user=kwargs['instance'])
            new_profile.save()
        except (KeyError, ValueError):
            msg = 'Unable to create ImagerProfile for {}'
            logger.error(msg.format(kwargs['instance']))


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_imager_profile(sender, **kwargs):
    try:
        kwargs['instance'].profile.delete()
    except (KeyError, AttributeError):
        msg = (
            "ImagerProfile instance not deleted for {}. "
            "Perhaps it does not exist?"
        )
        logger.warn(msg.format(kwargs['instance']))
