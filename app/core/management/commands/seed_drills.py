import json
import os
import sys
from django.core.management.base import BaseCommand
from core.models import Drill


class Command(BaseCommand):
    help = "Seed the database with drill data"

    def handle(self, *args, **options):
        # Load the JSON data
        json_file_path = os.path.join(
            os.path.dirname(__file__), 'drillSeeds.json')
        with open(json_file_path, 'r') as file:
            drills_data = json.load(file)

        for drill in drills_data:
            print(f"Processing drill: {drill['name']}")
            print(f"Name length: {len(drill['name'])}")
            print(f"Instructions length: {len(drill['instructions'])}")
            print(f"Type length: {len(drill['type'])}")

            try:
                Drill.objects.create(
                    name=drill['name'],
                    maxScore=drill['maxScore'],
                    instructions=drill['instructions'],
                    image=drill['image'],
                    type=drill['type'],
                    skills=drill['skills'],
                    layoutMaxScore=drill.get('layoutMaxScore', None),
                    attempts=drill.get('attempts', None),
                    layouts=drill.get('layouts', None),
                )
            except Exception as e:
                print(f"Error saving drill: {drill['name']}")
                print(f"Exception: {e}")
                sys.exit(1)
