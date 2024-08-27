from django.core.management.base import BaseCommand
from core.models import Drill, TableSetup, DrillSet


class Command(BaseCommand):
    help = "Seed the database with drill data"

    def handle(self, *args, **options):
        # Clear Drills and TableSetups
        Drill.objects.all().delete()
        TableSetup.objects.all().delete()
        DrillSet.objects.all().delete()
        print("Cleared Drills and TableSetups")
