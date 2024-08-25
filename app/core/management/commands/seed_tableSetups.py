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

                # Check for optional fields and provide placeholders if missing
                ball_position_props = setup.get(
                    'ballPositionProps',
                    {
                        'number': 0,
                        'x': 4,
                        'y': 1
                    }
                )
                potting_pocket_prop = setup.get(
                    'pottingPocketProp',
                    {
                        "show": False,
                        'x': 8,
                        'y': 4
                    }
                )
                target_specs = setup.get(
                    'targetSpecs',
                    {
                        'isTarget': False,
                        'x': 7.5,
                        'y': 0.5,
                        'rotate': False,
                        'w': 0.65,
                        'h': 0.8
                    }
                )
                leave_line_prop = setup.get(
                    'leaveLineProp',
                    {
                        'draw': False,
                        'x': 0,
                        'y': 0
                    }
                )
                kick_shot_line_prop = setup.get(
                    'kickShotLineProp',
                    {
                        'draw': False,
                        'rails': 0,
                        'objectBall': 0,
                    }
                )
                bank_shot_line_prop = setup.get(
                    'bankShotLineProp',
                    {
                        'draw': False,
                        'objectBall': 0,
                        'pocket': {
                            'x': 8,
                            'y': 0
                        }
                    }
                )

                # Create the TableSetup object with the corresponding drill_id
                TableSetup.objects.create(
                    drill=drill,
                    drillName=drill.name,
                    ballPositionProps=ball_position_props,
                    pottingPocketProp=potting_pocket_prop,
                    startIndex=setup.get('startIndex', 0),
                    showShotLine=setup.get('showShotLine', False),
                    targetSpecs=target_specs,
                    leaveLineProp=leave_line_prop,
                    kickShotLineProp=kick_shot_line_prop,
                    bankShotLineProp=bank_shot_line_prop,
                )
            except Drill.DoesNotExist:
                print(f"Drill with name '{drill_name}' does not exist.")
                sys.exit(1)
            except Exception as e:
                print(f"Error saving setup for drill '{drill_name}'")
                print(f"Exception: {e}")
                sys.exit(1)
