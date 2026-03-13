from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0028_contactthread_contactmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogentry",
            name="hide_from_web",
            field=models.BooleanField(default=False),
        ),
    ]
