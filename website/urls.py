from django.urls import path

from . import views


app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("story/", views.story, name="story"),
    path("gallery/", views.gallery, name="gallery"),
    path("team/", views.team, name="team"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("robots.txt", views.robots_txt, name="robots"),
]
