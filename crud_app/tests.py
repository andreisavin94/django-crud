from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crud_app.models import Profile


class LoggedInUserMixin:
    url = None

    def test_redirect_if_user_not_logged_in(self):
        redirect_url = f"{reverse('social:begin', args=['github'])}?next={self.url}"
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.url, redirect_url)


class TestIndexView(LoggedInUserMixin, TestCase):
    def setUp(self):
        self.url = reverse("index_view")
        self.user = User.objects.create()
        self.client.force_login(user=self.user)
        self.profile = Profile.objects.create(
            user=self.user, name="John Doe", phone="12345", address="Nowhere"
        )

    def test_index_with_profile_created(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.profile.name)
        self.assertContains(response, self.profile.phone)
        self.assertContains(response, self.profile.address)

    def test_index_with_no_profile(self):
        Profile.objects.get(user=self.user).delete()

        response = self.client.get(self.url)

        self.assertContains(response, "You haven't created a profile yet")
