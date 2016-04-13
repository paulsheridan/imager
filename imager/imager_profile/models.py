from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings


class ActiveManager(models.Manager):
    """Ensure only active profiles are returned."""
    def get_queryset(self):
        qs = super(ActiveManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """Profile model."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile'
        )
    # following = models.ManyToManyField(
    #     'self',
    #     symmetrical=False,
    #     related_name='follower_of'
    #     )
    # region = models.CharField(default='', max_length=3, choices=REGIONS)
    camera = models.CharField(default='', max_length=30)
    # photography_type = models.CharField(default='', max_length=30, choices=PHOTO_TYPES)

    active = ActiveManager()
    objects = models.Manager()
