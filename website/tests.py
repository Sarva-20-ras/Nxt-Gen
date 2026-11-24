import re
from urllib.parse import unquote

from django.contrib.staticfiles import finders
from django.test import TestCase


class HomePageTests(TestCase):
    def test_google_site_verification_file_is_available_at_site_root(self):
        response = self.client.get("/googlea6c7eabbdc6922d8.html")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode(),
            "google-site-verification: googlea6c7eabbdc6922d8.html",
        )

    def test_homepage_renders_all_sections(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        sections = (
            "home",
            "about",
            "what-we-do",
            "leaders",
            "story",
            "team",
            "events",
            "outreach",
            "gallery",
            "join",
        )
        for section in sections:
            with self.subTest(section=section):
                self.assertContains(response, f'id="{section}"')

    def test_homepage_uses_django_static_assets(self):
        response = self.client.get("/")

        stylesheets = (
            "base.css",
            "hero.css",
            "navbar.css",
            "about.css",
            "story.css",
            "what-we-do.css",
            "events.css",
            "outreach.css",
            "gallery.css",
            "join.css",
            "footer.css",
            "animations.css",
            "leaders.css",
            "team.css",
            "responsive-tablet.css",
            "responsive-mobile.css",
        )
        rendered_stylesheets = re.findall(
            r'<link rel="stylesheet" href="([^"]+)"',
            response.content.decode(),
        )
        self.assertEqual(
            rendered_stylesheets,
            [f"/static/website/css/{stylesheet}" for stylesheet in stylesheets],
        )

        for stylesheet in stylesheets:
            path = f"website/css/{stylesheet}"
            with self.subTest(stylesheet=stylesheet):
                self.assertContains(response, f"/static/{path}")
                self.assertIsNotNone(finders.find(path), f"Missing stylesheet: {path}")

        self.assertContains(response, "/static/website/js/site.js")
        self.assertContains(response, "/static/website/images/logo1.png")

        image_paths = {
            unquote(path)
            for path in re.findall(
                r'src="/static/([^"]+)"',
                response.content.decode(),
            )
        }
        image_paths.update(("website/images/ff.png", "website/images/out.jpeg"))

        for path in sorted(image_paths):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path), f"Missing static asset: {path}")
