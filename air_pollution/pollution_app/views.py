from django.shortcuts import render
from django.http import JsonResponse
from .utils.data_fetchers import SatelliteDataFetcher, CPCBDataFetcher, MERRA2DataFetcher, GeoJSONFetcher
from .utils.data_processing import PMPredictionModel
from .models import SatelliteData, GroundMeasurement, AtmosphericData, PredictedPM, State, District
from datetime import datetime, timedelta, time
import random
import json
import math

def index(request):
    """Main page with interactive visualization"""
    today = datetime.now().strftime("%Y-%m-%d")
    return render(request, 'visualization.html', {'today': today})
def get_pollution_data(request):
    """API endpoint to get pollution data"""
    try:
        # Get parameters from request
        lat = float(request.GET.get('lat', 28.6))
        lon = float(request.GET.get('lon', 77.2))
        date = request.GET.get('date', datetime.now().strftime("%Y-%m-%d"))
        
        # Fetch data from various sources
        satellite_data = SatelliteDataFetcher.fetch_insat_aod_data(date)
        ground_data = CPCBDataFetcher.fetch_ground_pm_data()
        atmospheric_data = MERRA2DataFetcher.fetch_merra2_data(lat, lon, date)
        
        # Predict PM levels
        pm_model = PMPredictionModel()
        predicted_pm = pm_model.predict_pm(
            aod=satellite_data[0]['aod_value'] if satellite_data else 0.5,
            temp=atmospheric_data['temperature'] if atmospheric_data else 25.0,
            humidity=atmospheric_data['humidity'] if atmospheric_data else 60.0,
            wind_speed=atmospheric_data['wind_speed'] if atmospheric_data else 5.5
        )
        
        # Prepare response
        response_data = {
            'satellite_data': satellite_data,
            'ground_data': ground_data,
            'atmospheric_data': atmospheric_data,
            'predicted_pm2_5': predicted_pm,
            'timestamp': datetime.now().isoformat()
        }
        
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_geojson_data(request):
    """API endpoint to get GeoJSON data for India"""
    try:
        level = request.GET.get('level', 'state')  # 'state' or 'district'
        name = request.GET.get('name', None)
        
        if level == 'state':
            if name:
                state = State.objects.get(name=name)
                return JsonResponse({'type': 'FeatureCollection', 'features': json.loads(state.geojson_data)})
            else:
                states = State.objects.all()
                features = []
                for state in states:
                    features.extend(json.loads(state.geojson_data)['features'])
                return JsonResponse({'type': 'FeatureCollection', 'features': features})
        elif level == 'district':
            if name:
                district = District.objects.get(name=name)
                return JsonResponse({'type': 'FeatureCollection', 'features': json.loads(district.geojson_data)})
            else:
                districts = District.objects.all()
                features = []
                for district in districts:
                    features.extend(json.loads(district.geojson_data)['features'])
                return JsonResponse({'type': 'FeatureCollection', 'features': features})
        else:
            return JsonResponse({'error': 'Invalid level parameter'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.http import JsonResponse
from datetime import datetime, timedelta
import random

def get_pm_predictions(request):
    """API endpoint to get PM predictions for visualization"""
    try:
        is_live = request.GET.get('live', 'false').lower() == 'true'
        
        if is_live:
            # Live mode - generate current data with small random variations
            date_str = datetime.now().strftime("%Y-%m-%d")
            timestamp = datetime.now().isoformat()
            
            # Add some randomness to simulate real-time changes
            base_variation = random.uniform(0.9, 1.1)
            time_variation = 0.5 + 0.5 * math.sin(time.time() / 3600)  # Varies slowly over time
        else:
            # Historical mode
            date_str = request.GET.get('date', datetime.now().strftime("%Y-%m-%d"))
            date = datetime.strptime(date_str, "%Y-%m-%d")
            timestamp = date.isoformat()
            base_variation = 1.0
            time_variation = 1.0
        # Major Indian cities with their precise coordinates
        cities = [
            {'name': 'Delhi', 'lat': 28.6139, 'lon': 77.2090},
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
            {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946},
            {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639},
            {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707},
            {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867},
            {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567},
            {'name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714},
            {'name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873},
            {'name': 'Lucknow', 'lat': 26.8467, 'lon': 80.9462},
            {'name': 'Kanpur', 'lat': 26.4499, 'lon': 80.3319},
            {'name': 'Nagpur', 'lat': 21.1458, 'lon': 79.0882},
            {'name': 'Indore', 'lat': 22.7196, 'lon': 75.8577},
            {'name': 'Thane', 'lat': 19.2183, 'lon': 72.9781},
            {'name': 'Bhopal', 'lat': 23.2599, 'lon': 77.4126},
            {'name': 'Visakhapatnam', 'lat': 17.6868, 'lon': 83.2185},
            {'name': 'Patna', 'lat': 25.5941, 'lon': 85.1376},
            {'name': 'Vadodara', 'lat': 22.3072, 'lon': 73.1812},
            {'name': 'Ghaziabad', 'lat': 28.6692, 'lon': 77.4538},
            {'name': 'Ludhiana', 'lat': 30.9010, 'lon': 75.8573}
        ]
        
        # Generate predictions with seasonal variation
        predictions = []
        for city in cities:
            # Base PM2.5 value with some randomness
            base_pm = random.uniform(50, 150) * base_variation * time_variation
            
            # Seasonal variation (higher in winter months)
             # Seasonal variation (higher in winter months)
            month = datetime.now().month
            if month in [11, 12, 1, 2]:  # Winter
                base_pm *= 1.3
            elif month in [5, 6, 7, 8]:  # Monsoon
                base_pm *= 0.7
                
            # Add some location-specific variation
            loc_variation = 0.8 + 0.4 * (hash(city['name']) % 100) / 100
            pm2_5 = round(base_pm * loc_variation, 1)

            predictions.append({
                'location': city['name'],
                'lat': city['lat'],
                'lon': city['lon'],
                'pm2_5': pm2_5,
                'pm10': round(pm2_5 * (1.2 + random.random() * 0.6), 1), # PM10 is typically higher than PM2.5
                'wind_speed': round(random.uniform(5, 15) * base_variation, 1),
                'humidity': random.randint(40, 90),
                'temperature': random.randint(15, 35),
                'timestamp': timestamp,
                'confidence': round(random.uniform(70, 95), 1)
            })
        
        # Generate trend data for the last 7 days
        trend_data = []
        for i in range(7 if not is_live else 24, 0, -1):
            if is_live:
                trend_date = datetime.now() - timedelta(hours=i)
                time_factor = 0.8 + 0.4 * math.sin((time.time() - i*3600) / 3600 / 6)
            else:
                trend_date = date - timedelta(days=i)
                time_factor = 1.0
            # # Similar variation logic for trend data
            # base_pm = random.uniform(50, 150)
            # month = trend_date.month
            # if month in [11, 12, 1, 2]:
            #     base_pm *= 1.3
            # elif month in [5, 6, 7, 8]:
            #     base_pm *= 0.7
            # daily_variation = random.uniform(0.8, 1.2)
            trend_pm = round(base_pm * (0.9 + 0.2 * (i/7)) * time_factor, 1)
            
            trend_data.append({
                'date': trend_date.isoformat(),
                'pm2_5': trend_pm
            })
        
        return JsonResponse({
            'predictions': predictions,
            'trend': trend_data,
            'date': date_str,
            'is_live': is_live
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)