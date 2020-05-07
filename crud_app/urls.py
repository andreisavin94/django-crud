from django.urls import path

from crud_app.views import (
    IndexView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
]
