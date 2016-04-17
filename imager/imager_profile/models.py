from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings


PHOTOGRAPHY_TYPES = [
    ('portrait', 'Portrait'),
    ('landscape', 'Landscape'),
]


class ActiveManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                null=False)
    region = models.CharField(default='us', max_length=30)
    bio = models.TextField(default='')
    camera = models.TextField(default='')
    photography_type = models.CharField(max_length=30, default='portrait',
                                        choices=PHOTOGRAPHY_TYPES)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='friend_of')
    objects = models.Manager()
    active = ActiveManager()

    @property
    def is_active(self):
        return self.user.is_active
