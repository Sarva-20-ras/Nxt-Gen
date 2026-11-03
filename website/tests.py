import re
from urllib.parse import unquote

from django.contrib.staticfiles import finders
from django.test import TestCase


class HomePageTests(TestCase):
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

        self.assertContains(response, "/static/website/css/site.css")
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
