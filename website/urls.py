from django.urls import path

from . import views


app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "googlea6c7eabbdc6922d8.html",
        views.google_site_verification,
        name="google-site-verification",
    ),
]
