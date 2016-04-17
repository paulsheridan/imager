from django.test import TestCase
from django.contrib.auth.models import User
from .models import Album, Image
from datetime import datetime
from django.db.models.fields.files import ImageFieldFile
import factory
import os
from imager.settings import BASE_DIR


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    photo = factory.django.ImageField(color='blue')


class TestImages(TestCase):
    """Verify link between album and image"""
    def setUp(self):
        self.test_user1 = User.objects.create_user('test user',
                                                   'test@test.com',
                                                   'testpassword')
        self.test_user1.save()
        self.album1 = Album(title='album1', owner=self.test_user1)
        self.album2 = Album(title='album2', owner=self.test_user1)
        self.image1 = PhotoFactory.create(title='image1',
                                          owner=self.test_user1)
        self.image2 = PhotoFactory.create(title='image2',
                                          owner=self.test_user1)
        self.album1.save()
        self.album2.save()

        self.image1.save()
        self.image2.save()

        self.image1.albums.add(self.album1)

    # def tearDown(self):
    #     os.remove(os.path.join(BASE_DIR,
    #                            '/{}'.format(self.image1.photo.url)))
    #     os.remove(os.path.join(BASE_DIR,
    #                            '/{}'.format(self.image2.photo.url)))

    def test_album_exists(self):
        """Verify album has been created"""
        self.assertIsInstance(self.album1, Album)

    def test_image_exists(self):
        """Verify image has been created"""
        self.assertIsInstance(self.image1, Image)

    def test_album_title(self):
        """Verify album title exists"""
        self.assertEquals(self.album1.title, 'album1')

    def test_image_title(self):
        """Verify image title"""
        self.assertEquals(self.image1.title, 'image1')

    def test_image_in_album(self):
        """Test to verify that image can be in album"""
        self.assertEquals(self.album1.images.all()[0], self.image1)

    def test_user_album_in_user(self):
        """Verify album user relationship"""
        self.assertEquals(self.test_user1.albums.all().count(), 2)

    def test_user_has_both_images(self):
        """Verify user album relationship"""
        self.assertEquals(self.test_user1.images.all().count(), 2)

    def test_image_has_both_image(self):
        """Verify file associated with photo instance"""
        self.assertIsInstance(self.image1.photo, ImageFieldFile)

    def test_album_default_description(self):
        """Verify album name default"""
        self.assertEquals(self.album1.description, '')

    def test_image_description(self):
        """Verify image name default"""
        self.assertEquals(self.image1.description, '')

    def test_album_uploaded(self):
        """Verify upload date"""
        self.assertIsInstance(self.album1.date_uploaded, datetime)

    def test_image_uploaded(self):
        """Verify image date uploaded"""
        self.assertIsInstance(self.image1.date_uploaded, datetime)

    def test_album_modified(self):
        """Verify new modification date"""
        initial = self.image1.date_modified
        self.assertEquals(initial, self.image1.date_modified)
        self.image1.title = 'new title'
        self.image1.save()
        self.assertNotEqual(initial, self.image1.date_modified)
