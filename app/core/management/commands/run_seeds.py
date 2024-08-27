from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Seed the database with all drill data"

    def handle(self, *args, **options):
        # Call command clear_db to clear all drills and drill scores
        print("Clearing Drills and DrillScores")
        call_command('clear_db')
        call_command('seed_drills')
        call_command('seed_tableSetups')
        call_command('seed_drill_sets')
        print("Seeded Drills and TableSetups")
