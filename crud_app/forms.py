from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from crud_app.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "phone", "address"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user

        return super().save(commit)
