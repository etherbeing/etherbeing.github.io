from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0020_blogentry_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="github_access_token",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="user",
            name="github_login",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="user",
            name="github_token_scope",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
