from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings


PUBLIC_OPTIONS = (
    ('private', 'Private'),
    ('shared', 'Shared'),
    ('public', 'Public'),
)


@python_2_unicode_compatible
class Album(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='albums',
                              null=True)
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=7, choices=PUBLIC_OPTIONS,
                                 default='Private')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='images',
                              null=True)
    photo = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=7, choices=PUBLIC_OPTIONS,
                                 default='private')
    albums = models.ManyToManyField(Album, related_name='images')

    def __str__(self):
        return self.title
