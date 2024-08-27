import json
import os
import sys
from django.core.management.base import BaseCommand
from core.models import Drill, DrillSet
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

            # Fetch drills by name
            drill_objects = []
            for drill_name in drill_set['drills']:
                drill = all_drills.filter(name=drill_name).first()
                if drill:
                    drill_objects.append(drill)
                else:
                    print(f"Drill not found: {drill_name}")
                    continue  # Skip the drill if not found

            if not drill_objects:
                print(
                    f"No valid drills found for drill set: {drill_set['name']}")
                continue

            # Create the DrillSet and add drills to it
            try:
                drill_set_obj = DrillSet.objects.create(
                    name=drill_set['name'],
                    createdBy=default_user
                )
                drill_set_obj.drills.add(*drill_objects)
            except Exception as e:
                print(f"Error saving drill set: {drill_set['name']}")
                print(f"Exception: {e}")
                sys.exit(1)
