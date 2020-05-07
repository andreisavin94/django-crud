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


class TestUpdateProfile(LoggedInUserMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create()
        profile = Profile.objects.create(
            user=self.user, name="John Doe", phone="12345", address="Nowhere"
        )
        self.url = reverse("update_profile_view", args=[profile.pk])
        self.client.force_login(user=self.user)
        self.form_data = {
            "name": "Michael Doe",
            "phone": "98765",
            "address": "Somewhere",
        }

    def test_update(self):
        response = self.client.post(self.url, data=self.form_data)

        self.assertRedirects(response, reverse("index_view"))
        self.assertEqual(Profile.objects.filter(user=self.user).count(), 1)
        profile = Profile.objects.first()
        self.assertEqual(profile.name, self.form_data["name"])
        self.assertEqual(profile.phone, self.form_data["phone"])
        self.assertEqual(profile.address, self.form_data["address"])

    def test_update_with_missing_required_field(self):
        self.form_data.pop("name")

        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        profile = Profile.objects.first()
        self.assertEqual(profile.name, "John Doe")

    def test_update_with_invalid_field(self):
        self.form_data["foo"] = "bar"

        self.client.post(self.url, data=self.form_data)

        profile = Profile.objects.first()
        self.assertEqual(profile.name, self.form_data["name"])
        self.assertEqual(profile.phone, self.form_data["phone"])
        self.assertEqual(profile.address, self.form_data["address"])

    def test_update_other_profile(self):
        user_two = User.objects.create(username="Two")
        profile_two = Profile.objects.create(user=user_two, name="Foo Bar")
        url = reverse("update_profile_view", args=[profile_two.pk])

        response = self.client.post(url, data=self.form_data)

        self.assertEqual(response.status_code, 404)

    def test_update_invalid_profile(self):
        url = reverse("update_profile_view", args=[999])

        response = self.client.post(url, data=self.form_data)

        self.assertEqual(response.status_code, 404)


class TestDeleteProfile(LoggedInUserMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create()
        profile = Profile.objects.create(
            user=self.user, name="John Doe", phone="12345", address="Nowhere"
        )
        self.url = reverse("delete_profile_view", args=[profile.pk])
        self.client.force_login(user=self.user)

    def test_delete(self):
        response = self.client.post(self.url, data={})

        self.assertRedirects(response, reverse("index_view"))
        self.assertEqual(Profile.objects.count(), 0)

    def test_delete_other_profile(self):
        user_two = User.objects.create(username="Two")
        profile_two = Profile.objects.create(user=user_two, name="Foo Bar")
        url = reverse("delete_profile_view", args=[profile_two.pk])

        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Profile.objects.count(), 2)

    def test_delete_invalid_profile(self):
        url = reverse("delete_profile_view", args=[999])

        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Profile.objects.count(), 1)
