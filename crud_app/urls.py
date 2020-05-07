from django.urls import path

from crud_app.views import (
    IndexView,
    CreateProfileView,
    UpdateProfileView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
    path("profile/create/", CreateProfileView.as_view(), name="create_profile_view"),
    path(
        "profile/<int:pk>/update/",
        UpdateProfileView.as_view(),
        name="update_profile_view",
    ),
]
