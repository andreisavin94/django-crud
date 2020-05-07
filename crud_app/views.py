from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.urls import reverse_lazy


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    login_url = reverse_lazy("social:begin", args=["github"])
