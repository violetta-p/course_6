from django.core.management import BaseCommand
from scheduler.scheduler import start_job


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_job()
