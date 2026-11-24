from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")


def google_site_verification(request):
    return HttpResponse(
        "google-site-verification: googlea6c7eabbdc6922d8.html",
        content_type="text/plain",
    )
