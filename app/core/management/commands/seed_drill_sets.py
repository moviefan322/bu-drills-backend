import json
import os
import sys
from django.core.management.base import BaseCommand
from core.models import Drill, DrillSet, DrillSetMembership
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with drill set data"

    def handle(self, *args, **options):
        # Load the JSON data
        json_file_path = os.path.join(
            os.path.dirname(__file__), 'drillSetSeeds.json')
        with open(json_file_path, 'r') as file:
            drill_sets_data = json.load(file)

        # Get all drills and users beforehand
        all_drills = Drill.objects.all()
        default_user = User.objects.get(pk=1)  # Fetch default user by ID

        for drill_set in drill_sets_data:
            print(f"Processing drill set: {drill_set['name']}")

            # Create the DrillSet object
            try:
                drill_set_obj = DrillSet.objects.create(
                    name=drill_set['name'],
                    createdBy=default_user
                )

                # Create DrillSetMembership for each drill in the set
                for index, drill_name in enumerate(drill_set['drills']):
                    drill = all_drills.filter(name=drill_name).first()
                    if drill:
                        DrillSetMembership.objects.create(
                            drill=drill,
                            drill_set=drill_set_obj,
                            position=index + 1  # Positions are 1-based
                        )
                    else:
                        print(f"Drill not found: {drill_name}")
                        continue  # Skip the drill if not found

            except Exception as e:
                print(f"Error saving drill set: {drill_set['name']}")
                print(f"Exception: {e}")
                sys.exit(1)
