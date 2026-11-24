from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from .validators import validate_image_size


IMAGE_VALIDATORS = [
    FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]),
    validate_image_size,
]


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="team/",
        blank=True,
        help_text="Optional. Upload a JPG, PNG, or WebP image up to 4 MB.",
        validators=IMAGE_VALIDATORS,
    )
    legacy_image_path = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class GalleryPhoto(models.Model):
    caption = models.CharField(max_length=160)
    alt_text = models.CharField(
        max_length=200,
        help_text="Describe the photo for visitors using screen readers.",
    )
    image = models.ImageField(
        upload_to="gallery/",
        blank=True,
        help_text="Use a photo you have permission to publish. Maximum size: 4 MB.",
        validators=IMAGE_VALIDATORS,
    )
    legacy_image_path = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(
        default=False,
        help_text="New uploads stay hidden until a publisher approves them.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="submitted_gallery_photos",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="approved_gallery_photos",
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        permissions = [
            ("publish_galleryphoto", "Can approve gallery photos"),
        ]

    def __str__(self):
        return self.caption

    def clean(self):
        super().clean()
        if not self.image and not self.legacy_image_path:
            raise ValidationError({"image": "Add a photo before saving this gallery entry."})
