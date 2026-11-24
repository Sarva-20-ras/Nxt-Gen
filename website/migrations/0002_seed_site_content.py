from django.db import migrations


TEAM_MEMBERS = [
    (
        "Pariwesh Rai",
        "Team Coordinator",
        "Coordinates the entire team and helps lead worship.",
        "website/images/pariwesh.jpeg",
    ),
    (
        "Esha Chettri",
        "Assistant Team Coordinator",
        "Keeps everyone involved; serves in worship, media, photography, and content.",
        "website/images/esha.jpeg",
    ),
    (
        "Saru Tamamg",
        "Worship Team",
        "Helps lead worship and serves as an usher.",
        "website/images/saru.jpeg",
    ),
    (
        "Sarvajeet Rasaily",
        "Worship & Media",
        "Helps organize the projection and content teams and leads worship.",
        "website/images/sarva.jpeg",
    ),
    (
        "Siyon Mothay",
        "Worship Team",
        "Helps lead worship on drums and serves as an usher.",
        "website/images/siyon.jpeg",
    ),
    (
        "Prakrit Shankar",
        "Worship Team",
        "Serves as a bassist and usher and helps lead worship.",
        "website/images/prakrit.jpeg",
    ),
    (
        "Amos Sewa",
        "Worship Team",
        "Helps across the worship service and serves as an usher.",
        "website/images/amos.jpeg",
    ),
    (
        "Mercy Chhetri",
        "Media Team",
        "Serves in media, design, photography, content, and worship.",
        "website/images/mercy.jpeg",
    ),
    (
        "Evan Mangrati",
        "Worship Team",
        "Helps with drums during worship and serves as an usher.",
        "website/images/Evan.jpeg",
    ),
    (
        "Isaiah Peter Baraily",
        "Projection Team",
        "Serves in media, projection, and related activities.",
        "website/images/Isaiah.jpeg",
    ),
    (
        "Emmanuel Rai",
        "Usher",
        "Serves as an usher and in the worship team.",
        "website/images/emmanuel.jpeg",
    ),
    (
        "Anita Bhutia",
        "Usher",
        "Handles registration and administrative tasks.",
        "website/images/anita.jpeg",
    ),
    (
        "Rose Jajoo",
        "Nurse / Usher",
        "Supports health-related needs and serves as an usher.",
        "website/images/Rose.jpeg",
    ),
    (
        "Shakuntala Limboo",
        "Usher",
        "Handles registration and administrative tasks.",
        "website/images/sakuntala.jpeg",
    ),
    (
        "Lakpa Sherpa",
        "Usher",
        "Handles administrative tasks and supports the team.",
        "website/images/lakpa.jpeg",
    ),
    (
        "Jonah Lama",
        "Usher",
        "Serves with a passion for helping others.",
        "",
    ),
    (
        "James Rai",
        "Usher",
        "Serves with a passion for helping others.",
        "",
    ),
    (
        "Shekinah Peter Baraily",
        "Usher",
        "Serves with a passion for helping others.",
        "",
    ),
]

GALLERY_PHOTOS = [
    ("Worship Team 2026", "NextGen worship team in 2026.", "website/images/w2.jpeg"),
    ("Next_Gen 2026", "NextGen members together in 2026.", "website/images/group1.jpeg"),
    ("Next_Gen 2025", "NextGen members together in 2025.", "website/images/gp.JPG"),
    (
        "Next_Gen 2025 ft. Rajat bk. & Team",
        "NextGen members with Rajat and team in 2025.",
        "website/images/rajat.JPG",
    ),
    ("Worship Team A 2025", "Worship Team A in 2025.", "website/images/wor2.JPG"),
    ("Worship Team B 2025", "Worship Team B in 2025.", "website/images/wor1.JPG"),
    ("Next_Gen 2024", "NextGen members together in 2024.", "website/images/ff.png"),
    ("Worship Team 2024", "NextGen worship team in 2024.", "website/images/out.jpeg"),
    ("Next_Gen 2023", "NextGen members together in 2023.", "website/images/group 2.jpeg"),
    (
        "Next_Gen ft. Samir Tiruwa",
        "NextGen members with Samir Tiruwa.",
        "website/images/Worship Team.jpeg",
    ),
]


def seed_content(apps, schema_editor):
    TeamMember = apps.get_model("website", "TeamMember")
    GalleryPhoto = apps.get_model("website", "GalleryPhoto")

    for sort_order, (name, role, bio, image_path) in enumerate(TEAM_MEMBERS, start=1):
        TeamMember.objects.get_or_create(
            name=name,
            defaults={
                "role": role,
                "bio": bio,
                "legacy_image_path": image_path,
                "sort_order": sort_order * 10,
                "is_active": True,
            },
        )

    for sort_order, (caption, alt_text, image_path) in enumerate(GALLERY_PHOTOS, start=1):
        GalleryPhoto.objects.get_or_create(
            caption=caption,
            defaults={
                "alt_text": alt_text,
                "legacy_image_path": image_path,
                "sort_order": sort_order * 10,
                "is_published": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]
