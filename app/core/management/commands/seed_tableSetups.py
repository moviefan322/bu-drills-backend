import json
import os
import sys
from django.core.management.base import BaseCommand
from core.models import Drill, TableSetup


class Command(BaseCommand):
    help = "Seed the database with setup data"

    def handle(self, *args, **options):
        # Load the JSON data
        json_file_path = os.path.join(
            os.path.dirname(__file__), 'tableSetupSeeds.json')
        with open(json_file_path, 'r') as file:
            setups_data = json.load(file)

        for setup in setups_data:
            try:
                # Log the drillName for better traceability
                drill_name = setup.get('drillName', 'Unknown Drill Name')
                print(f"Processing setup for drill: {drill_name}")

                # Find the drill matching the drillName
                drill = Drill.objects.get(name=drill_name)
                print(f"Found drill with name: {drill_name}")
                print(f"Drill ID: {drill.id}")
                drill_name = drill.name

                # Create the TableSetup object with the corresponding drill_id
                TableSetup.objects.create(
                    drill=drill,
                    drillName=drill.name,
                    ballPositionProps=setup['ballPositionProps'],
                    pottingPocketProp=setup['pottingPocketProp'],
                    startIndex=setup['startIndex'],
                    showShotLine=setup['showShotLine'],
                    targetSpecs=setup['targetSpecs'],
                    leaveLineProp=setup['leaveLineProp'],
                    kickShotLineProp=setup['kickShotLineProp'],
                    bankShotLineProp=setup['bankShotLineProp'],
                )
            except Drill.DoesNotExist:
                print(f"Drill with name '{drill_name}' does not exist.")
                sys.exit(1)
            except Exception as e:
                print(f"Error saving setup for drill '{drill_name}'")
                print(f"Exception: {e}")
                sys.exit(1)
