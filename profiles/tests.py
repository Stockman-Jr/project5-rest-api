from django.contrib.auth.models import User
from .models import TrainerProfile
from rest_framework import status
from rest_framework.test import APITestCase


class TrainerProfileListViewTests(APITestCase):
    def setUp(self):
        lily = User.objects.create_user(username='lily', password='pass')

    def test_can_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrainerProfileDetailViewTests(APITestCase):
    def setUp(self):
        lily = User.objects.create_user(username='lily', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')

    def test_can_retrieve_profile_with_valid_id(self):
        self.client.login(username='lily', password='pass')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_own_profile(self):
        self.client.login(username='lily', password='pass')
        response = self.client.put('/profiles/1/', {
            'owner': 'lily',
            'name': 'lillian',
            'bio': 'some text about lily'
        })
        profile = TrainerProfile.objects.filter(pk=1).first()
        self.assertEqual(profile.name, 'lillian')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_profile(self):
        self.client.login(username='lily', password='pass')
        response = self.client.put('/profiles/2/', {
            'owner': 'brian',
            'name': 'update brians name',
            'bio': 'update brians bio'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
