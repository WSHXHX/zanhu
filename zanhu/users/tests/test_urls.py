from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestUsersURLs(TestCase):

    def setUp(self):
        self.user = self.make_user()
        
    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail', kwargs={"username": "testuser"}), "/users/testuser/")

    def test_detail_resolve(self):
        self.assertEqual(resolve("/users/testuser/").view_name, "users:detail")

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'), "/users/~update/")

    def test_update_resolve(self):
        self.assertEqual(resolve("/users/~update/").view_name, "users:update")

    def test_redirect_reverse(self):
        self.assertEqual(reverse('users:redirect'), "/users/~redirect/")

    def test_redirect_resolve(self):
        self.assertEqual(resolve("/users/~redirect/").view_name, "users:redirect")



