from django.urls import path

from crud_app.views import (
    IndexView,
    CreateProfileView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
    path("profile/create/", CreateProfileView.as_view(), name="create_profile_view"),
]
