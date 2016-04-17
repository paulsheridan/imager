from django.test import TestCase
from .models import ImagerProfile
from django.contrib.auth.models import User


class TestProfile(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='person1',
            email='person1@email.com',
            password='password')
        self.user2 = User.objects.create_user(
            username='person2',
            email='person2@email.com',
            password='password')

        self.user1.save()
        self.user2.save()

    def test_new_user_exists(self):
        """Verify user creation"""
        self.assertEquals(len(User.objects.all()), 2)

    def test_new_profile_exists(self):
        """Verify profile creation"""
        self.assertEquals(len(ImagerProfile.objects.all()), 2)

    def test_profile_verify(self):
        """Verify profile matches one created"""
        self.assertEquals(ImagerProfile.objects.all()[0],
                          self.user1.profile)

    def test_profile_user(self):
        """Verify user matches one created"""
        profile = ImagerProfile.objects.all()[0]
        self.assertEquals(profile.user, self.user1)

    def test_user_deletion(self):
        """Verify profile deletion along with user deletion"""
        self.assertEquals(len(ImagerProfile.objects.all()), 2)
        self.user1.delete()
        self.assertEquals(len(ImagerProfile.objects.all()), 1)

    def test_profile_deletion(self):
        """Verify user is not deleted along with profile deletion"""
        self.assertEquals(len(User.objects.all()), 2)
        self.assertEquals(len(ImagerProfile.objects.all()), 2)
        self.user2.profile.delete()
        self.assertEquals(len(ImagerProfile.objects.all()), 1)
        self.assertEquals(len(User.objects.all()), 2)

    def test_profile_active(self):
        """Verify active profile"""
        self.assertEquals(self.user1.profile.is_active, True)

    def test_active_profiles(self):
        """Verify full list of profiles"""
        self.assertEquals(ImagerProfile.active.count(), 2)

    def test_friends(self):
        """Verify friendship connection between users"""
        p = self.user1.profile
        p.friends.add(self.user2)
        self.assertEquals(p.friends.all()[0], self.user2)
        self.assertEquals(self.user2.friend_of.all()[0],
                          self.user1.profile)
