from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.constants import roles
from accounts.models import Role

User = get_user_model()


class TestUserCreate(TestCase):
    def setUp(self) -> None:
        super(TestUserCreate, self).setUp()
        self.user_create_url = reverse('accounts:user_create')

        for _, role_name in roles.items():
            Role.objects.get_or_create(name=role_name)

        self.admin_role = Role.objects.get(name=roles.get('admin'))

        user = User.objects.create(username='test_client')
        user.set_password('adminadmin')
        user.save()
        user.profile.roles.add(self.admin_role.id)
        self.user = user

        self.client = Client()
        self.client.login(username='test_client', password='adminadmin')

    def test_create_user(self):
        response = self.client.post(self.user_create_url, {
            'username': 'test_user',
            'email': 'test_user@test.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'adminadmin',
            'role': [self.admin_role.id]

        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='test_user').exists())
        user = User.objects.get(username='test_user')
        self.assertEqual(user.first_name, 'test_first_name')
        self.assertTrue(user.check_password('adminadmin'))

    def test_no_required_role(self):
        self.user.profile.roles.remove(self.admin_role)
        response = self.client.post(self.user_create_url, {
            'username': 'test_user',
            'email': 'test_user@test.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'adminadmin',
            'role': [self.admin_role.id]

        })
        self.assertEqual(response.status_code, 403)
