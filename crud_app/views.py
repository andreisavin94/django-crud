from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from crud_app.forms import ProfileForm
from crud_app.models import Profile


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    login_url = reverse_lazy("social:begin", args=["github"])


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.filter(user=self.request.user).first()
        return context


class CreateProfileView(LoginRequiredMixin, CreateView):
    template_name = "create_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("index_view")

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "edit_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("index_view")

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "delete_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("index_view")

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
