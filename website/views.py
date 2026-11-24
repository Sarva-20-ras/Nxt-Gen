from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import GalleryPhoto, TeamMember


def home(request):
    return render(
        request,
        "website/home.html",
        {
            "team_members": TeamMember.objects.filter(is_active=True)[:5],
            "gallery_photos": GalleryPhoto.objects.filter(is_published=True)[:4],
        },
    )


def story(request):
    return render(request, "website/story_page.html")


def gallery(request):
    return render(
        request,
        "website/gallery_page.html",
        {
            "gallery_photos": GalleryPhoto.objects.filter(is_published=True),
            "full_page": True,
        },
    )


def team(request):
    return render(
        request,
        "website/team_page.html",
        {
            "team_members": TeamMember.objects.filter(is_active=True),
            "full_page": True,
        },
    )


def sitemap(request):
    site_url = settings.SITE_URL.rstrip("/")
    page_names = ("home", "story", "gallery", "team")
    locations = "".join(
        f"<url><loc>{escape(site_url + reverse(f'website:{name}'))}</loc></url>"
        for name in page_names
    )
    return HttpResponse(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{locations}</urlset>",
        content_type="application/xml",
    )


def robots_txt(request):
    return HttpResponse(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        f"Sitemap: {settings.SITE_URL.rstrip('/')}/sitemap.xml\n",
        content_type="text/plain",
    )
