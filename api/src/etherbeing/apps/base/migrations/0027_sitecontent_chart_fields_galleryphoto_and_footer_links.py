from django.db import migrations, models
import django.db.models.deletion


DEFAULT_GALLERY_PHOTOS = [
    {
        "title": "Etherbeing portrait",
        "image_url": "/gallery/esteban-chacon.jpg",
        "caption": "A first gallery frame from my personal collection, ready for expansion directly from the backend admin.",
    },
]


def seed_footer_links_and_gallery(apps, schema_editor):
    SiteContent = apps.get_model("base", "SiteContent")
    ContactGroup = apps.get_model("base", "ContactGroup")
    ContactLink = apps.get_model("base", "ContactLink")
    GalleryPhoto = apps.get_model("base", "GalleryPhoto")

    site_content = SiteContent.objects.filter(slug="primary").first()
    if site_content is None:
        return

    social_group = ContactGroup.objects.filter(
        site_content=site_content,
        title="Social Networks",
    ).first()
    if social_group is not None:
        next_order = ContactLink.objects.filter(group=social_group).count()
        ContactLink.objects.update_or_create(
            group=social_group,
            label="TradingView",
            defaults={
                "url": "https://www.tradingview.com/u/etherbeing/",
                "icon": "tradingview",
                "sort_order": next_order,
            },
        )

    for index, photo in enumerate(DEFAULT_GALLERY_PHOTOS):
        GalleryPhoto.objects.update_or_create(
            site_content=site_content,
            title=photo["title"],
            defaults={
                **photo,
                "sort_order": index,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0026_blogentry_category_publishedpost_blogentry_social_networks"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitecontent",
            name="featured_chart_symbol",
            field=models.CharField(default="BITSTAMP:ETHUSD", max_length=64),
        ),
        migrations.AddField(
            model_name="sitecontent",
            name="featured_chart_title",
            field=models.CharField(default="Ethereum / USD", max_length=255),
        ),
        migrations.CreateModel(
            name="GalleryPhoto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("image_url", models.CharField(max_length=500)),
                ("caption", models.TextField(blank=True, default="")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("site_content", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gallery_photos", to="base.sitecontent")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.RunPython(seed_footer_links_and_gallery, migrations.RunPython.noop),
    ]
