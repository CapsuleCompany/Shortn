from django.core.management.base import BaseCommand

from Shorten.consumers import AuthEventConsumer


class Command(BaseCommand):
    help = "Run the Shorten service Kafka consumer"

    def handle(self, *args, **options):
        self.stdout.write("Starting Shorten service consumer...")
        consumer = AuthEventConsumer()
        consumer.run()
