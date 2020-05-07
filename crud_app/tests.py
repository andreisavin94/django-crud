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


class TestCreateProfile(LoggedInUserMixin, TestCase):
    def setUp(self):
        self.url = reverse("create_profile_view")
        self.user = User.objects.create()
        self.client.force_login(user=self.user)
        self.form_data = {
            "name": "John Doe",
            "phone": "123456",
            "address": "King St",
        }

    def test_create_profile(self):
        response = self.client.post(self.url, data=self.form_data)

        self.assertRedirects(response, reverse("index_view"))
        self.assertEqual(Profile.objects.filter(user=self.user).count(), 1)
        created_profile = Profile.objects.get(user=self.user)
        self.assertEqual(created_profile.name, self.form_data["name"])
        self.assertEqual(created_profile.phone, self.form_data["phone"])
        self.assertEqual(created_profile.address, self.form_data["address"])

    def test_create_profile_with_name_missing(self):
        self.form_data.pop("name")

        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(Profile.objects.count(), 0)
        self.assertContains(response, "This field is required")

    def test_create_profile_with_name_blank(self):
        self.form_data["name"] = ""

        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(Profile.objects.count(), 0)
        self.assertContains(response, "This field is required")
