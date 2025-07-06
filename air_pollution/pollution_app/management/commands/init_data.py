from django.core.management.base import BaseCommand
from pollution_app.models import State, District
import json

class Command(BaseCommand):
    help = 'Initialize database with sample state and district data'
    
    def handle(self, *args, **kwargs):
        # Sample state data (in a real app, you would load actual GeoJSON)
        states = [
            {
                'name': 'Delhi',
                'geojson': {
                    'type': 'FeatureCollection',
                    'features': [
                        {
                            'type': 'Feature',
                            'properties': {'name': 'Delhi'},
                            'geometry': {
                                'type': 'Polygon',
                                'coordinates': [[[77.0, 28.6], [77.1, 28.6], [77.1, 28.7], [77.0, 28.7], [77.0, 28.6]]]
                            }
                        }
                    ]
                }
            }
        ]
        
        # Sample district data for Delhi
        delhi_districts = [
            {
                'name': 'Central Delhi',
                'geojson': {
                    'type': 'FeatureCollection',
                    'features': [
                        {
                            'type': 'Feature',
                            'properties': {'name': 'Central Delhi'},
                            'geometry': {
                                'type': 'Polygon',
                                'coordinates': [[[77.2, 28.6], [77.3, 28.6], [77.3, 28.7], [77.2, 28.7], [77.2, 28.6]]]
                            }
                        }
                    ]
                }
            }
        ]
        
        # Create states and districts
        for state_data in states:
            state, created = State.objects.get_or_create(
                name=state_data['name'],
                defaults={'geojson_data': json.dumps(state_data['geojson'])}
            )
            
            if state.name == 'Delhi':
                for district_data in delhi_districts:
                    District.objects.get_or_create(
                        state=state,
                        name=district_data['name'],
                        defaults={'geojson_data': json.dumps(district_data['geojson'])}
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized sample state and district data'))