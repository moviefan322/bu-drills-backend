from django.core.management.base import BaseCommand
from models import Drill

class Command(BaseCommand):
    help = 'Seeds the database with preset drills'

    def handle(self, *args, **kwargs):
        drills = [
            {'name': 'Freestyle Technique', 'description': 'Improving freestyle stroke technique.'},
            {'name': 'Backstroke Kick', 'description': 'Focus on backstroke kicking.'},
            {'name': 'Breaststroke Timing', 'description': 'Work on the timing of your breaststroke.'},
            # Add more drills as needed
        ]

        for drill in drills:
            Drill.objects.get_or_create(name=drill['name'], defaults={'description': drill['description']})

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with drills'))
