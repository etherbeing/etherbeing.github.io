from django.core.management.base import BaseCommand

from apps.base.seed_data import initialize_site_content


class Command(BaseCommand):
    help = "Initialize the default site content used by the frontend."

    def handle(self, *args, **options):
        site_content = initialize_site_content()
        self.stdout.write(
            self.style.SUCCESS(
                f"Site content '{site_content.slug}' initialized successfully."
            )
        )
