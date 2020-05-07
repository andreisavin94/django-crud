from django.urls import reverse


class LoggedInUserMixin:
    url = None

    def test_redirect_if_user_not_logged_in(self):
        redirect_url = f"{reverse('social:begin', args=['github'])}?next={self.url}"
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.url, redirect_url)
