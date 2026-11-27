import json
import re
from urllib.parse import unquote

from django.contrib import admin as django_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from .admin import GalleryPhotoAdmin
from .models import GalleryPhoto, TeamMember
from .validators import validate_image_size


class HomePageTests(TestCase):
    def test_homepage_renders_all_sections(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<meta name="google-site-verification" '
            'content="-OxL56_gDHXZqjhdZZ-WWSw-xcpxhEjF1wa_MlC8NZ0">',
        )
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
        self.assertContains(response, "/story/")
        self.assertContains(response, "/team/")
        self.assertContains(response, "/gallery/")
        self.assertContains(response, "Pariwesh Rai")
        self.assertContains(response, "Worship Team 2026")
        self.assertContains(response, "CHRISTMAS SEASON")

    def test_public_pages_have_canonical_and_search_metadata(self):
        pages = (
            ("", "NextGen in Christ | Christian Youth Community in Siliguri"),
            ("story/", "Our Story | NextGen in Christ, Siliguri"),
            ("team/", "Our Team | NextGen in Christ, Siliguri"),
            ("gallery/", "Gallery | NextGen in Christ, Siliguri"),
        )
        for path, title in pages:
            with self.subTest(path=path):
                response = self.client.get(f"/{path}")
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    f'<link rel="canonical" href="https://nextgeninchrist.vercel.app/{path}">',
                )
                self.assertContains(response, f"<title>{title}</title>")
                self.assertContains(response, 'property="og:title"')
                self.assertContains(response, 'name="twitter:card"')

    def test_homepage_has_valid_organization_structured_data(self):
        response = self.client.get("/")
        html = response.content.decode()
        match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            html,
            re.DOTALL,
        )

        self.assertIsNotNone(match)
        organization = json.loads(match.group(1))
        self.assertEqual(organization["@type"], "Organization")
        self.assertEqual(organization["url"], "https://nextgeninchrist.vercel.app")
        self.assertEqual(organization["areaServed"]["name"], "Siliguri")

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
            "pages.css",
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


class ContentPageTests(TestCase):
    def test_story_team_and_gallery_have_dedicated_pages(self):
        pages = (
            ("/story/", "BATON OF FAITH."),
            ("/team/", "Pariwesh Rai"),
            ("/gallery/", "Worship Team 2026"),
        )
        for path, content in pages:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, content)

    def test_unapproved_gallery_photos_are_hidden_until_approved(self):
        photo = GalleryPhoto.objects.create(
            caption="Pending review",
            alt_text="Photo waiting for review",
            legacy_image_path="website/images/w2.jpeg",
        )

        response = self.client.get("/gallery/")
        self.assertNotContains(response, "Pending review")

        photo.is_published = True
        photo.save()
        response = self.client.get("/gallery/")
        self.assertContains(response, "Pending review")

    def test_sitemap_and_robots_list_the_content_pages(self):
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap.status_code, 200)
        self.assertEqual(sitemap["Content-Type"], "application/xml")
        for path in ("", "story/", "gallery/", "team/"):
            self.assertContains(sitemap, f"https://nextgeninchrist.vercel.app/{path}")

        robots = self.client.get("/robots.txt")
        self.assertContains(robots, "Sitemap: https://nextgeninchrist.vercel.app/sitemap.xml")

    def test_admin_requires_an_authenticated_staff_account(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_staff_admin_can_open_team_and_gallery_management(self):
        user = get_user_model().objects.create_superuser(
            username="site-admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(user)

        for path in (
            "/admin/website/teammember/",
            "/admin/website/galleryphoto/add/",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_gallery_photo_cannot_be_published_without_approval_permission(self):
        editor = get_user_model().objects.create_user(
            username="gallery-editor",
            password="test-password",
            is_staff=True,
        )
        request = RequestFactory().post("/admin/")
        request.user = editor
        photo = GalleryPhoto(
            caption="Needs approval",
            alt_text="Photo awaiting approval",
            is_published=True,
        )

        GalleryPhotoAdmin(GalleryPhoto, django_admin.site).save_model(
            request,
            photo,
            form=None,
            change=False,
        )

        self.assertFalse(photo.is_published)
        self.assertEqual(photo.submitted_by, editor)

    def test_gallery_image_upload_limit_is_enforced(self):
        image = SimpleUploadedFile(
            "large.jpg",
            b"x" * (4 * 1024 * 1024 + 1),
            content_type="image/jpeg",
        )
        with self.assertRaises(ValidationError):
            validate_image_size(image)

    def test_gallery_publisher_records_approval(self):
        publisher = get_user_model().objects.create_user(
            username="gallery-publisher",
            password="test-password",
            is_staff=True,
        )
        permission = Permission.objects.get(codename="publish_galleryphoto")
        publisher.user_permissions.add(permission)
        request = RequestFactory().post("/admin/")
        request.user = publisher
        photo = GalleryPhoto(
            caption="Ready to publish",
            alt_text="Approved photo",
            legacy_image_path="website/images/w2.jpeg",
            is_published=True,
        )

        GalleryPhotoAdmin(GalleryPhoto, django_admin.site).save_model(
            request,
            photo,
            form=None,
            change=False,
        )

        self.assertTrue(photo.is_published)
        self.assertEqual(photo.approved_by, publisher)
        self.assertIsNotNone(photo.approved_at)

    def test_legacy_team_and_gallery_images_exist(self):
        for member in TeamMember.objects.exclude(legacy_image_path=""):
            with self.subTest(member=member.name):
                self.assertIsNotNone(finders.find(member.legacy_image_path))

        for photo in GalleryPhoto.objects.exclude(legacy_image_path=""):
            with self.subTest(photo=photo.caption):
                self.assertIsNotNone(finders.find(photo.legacy_image_path))

        user = get_user_model().objects.create_user(
            username="member",
            password="test-password",
        )
        self.client.force_login(user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])
