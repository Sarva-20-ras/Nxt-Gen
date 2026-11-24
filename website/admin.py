from django.contrib import admin, messages
from django.utils import timezone

from .models import GalleryPhoto, TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "bio")
    ordering = ("sort_order", "name")
    fields = ("name", "role", "bio", "image", "sort_order", "is_active")


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "caption",
        "is_published",
        "submitted_by",
        "approved_by",
        "created_at",
    )
    list_filter = ("is_published", "created_at")
    search_fields = ("caption", "alt_text")
    ordering = ("is_published", "sort_order", "-created_at")
    actions = ("approve_selected",)
    fields = (
        "caption",
        "alt_text",
        "image",
        "legacy_image_path",
        "sort_order",
        "is_published",
        "submitted_by",
        "approved_by",
        "approved_at",
    )
    readonly_fields = ("submitted_by", "approved_by", "approved_at")

    def has_publish_permission(self, request):
        return request.user.has_perm("website.publish_galleryphoto")

    @admin.action(
        description="Approve selected gallery photos",
        permissions=["publish"],
    )
    def approve_selected(self, request, queryset):
        now = timezone.now()
        photos = list(queryset.filter(is_published=False))
        for photo in photos:
            photo.is_published = True
            photo.approved_by = request.user
            photo.approved_at = now
            photo.updated_at = now
        GalleryPhoto.objects.bulk_update(
            photos,
            ("is_published", "approved_by", "approved_at", "updated_at"),
        )
        self.message_user(
            request,
            f"Approved {len(photos)} gallery photo(s).",
            messages.SUCCESS,
        )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not self.has_publish_permission(request):
            readonly.append("is_published")
        return readonly

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_published and not self.has_publish_permission(request):
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        can_publish = self.has_publish_permission(request)
        previous = None
        if change:
            previous = GalleryPhoto.objects.get(pk=obj.pk)
        else:
            obj.submitted_by = request.user

        if not can_publish:
            obj.is_published = False
        elif obj.is_published and (previous is None or not previous.is_published):
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        elif not obj.is_published:
            obj.approved_by = None
            obj.approved_at = None

        super().save_model(request, obj, form, change)
