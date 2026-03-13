from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0027_sitecontent_chart_fields_galleryphoto_and_footer_links"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactThread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=255)),
                ("status", models.CharField(choices=[("open", "Open"), ("replied", "Replied"), ("closed", "Closed")], default="open", max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_message_at", models.DateTimeField(auto_now_add=True)),
                ("requester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contact_threads", to="base.user")),
            ],
            options={"ordering": ["-last_message_at", "-id"]},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contact_messages", to="base.user")),
                ("thread", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="base.contactthread")),
            ],
            options={"ordering": ["created_at", "id"]},
        ),
    ]
