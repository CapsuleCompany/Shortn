from django.core.management.base import BaseCommand

from QR.consumers import AuthEventConsumer


class Command(BaseCommand):
    help = "Run the QR service Kafka consumer"

    def handle(self, *args, **options):
        self.stdout.write("Starting QR service consumer...")
        consumer = AuthEventConsumer()
        consumer.run()
