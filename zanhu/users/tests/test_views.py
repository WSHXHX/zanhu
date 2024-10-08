from django.test import RequestFactory
from test_plus.test import TestCase

from zanhu.users.views import UserUpdateView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()
   
class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        super().setUp()
        self.view = UserUpdateView()
        request = self.factory.get("/factory-url")
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEquals(self.view.get_success_url(), "/users/testuser/")

    def test_get_object(self):
        self.assertEquals(self.view.get_object(), self.user)
