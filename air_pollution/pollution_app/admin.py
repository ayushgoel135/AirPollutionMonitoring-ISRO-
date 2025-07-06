from django.contrib import admin
from .models import SatelliteData, GroundMeasurement, AtmosphericData, PredictedPM, State, District

@admin.register(SatelliteData)
class SatelliteDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'latitude', 'longitude', 'aod_value')
    list_filter = ('satellite_source',)
    search_fields = ('timestamp',)

@admin.register(GroundMeasurement)
class GroundMeasurementAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'timestamp', 'pm2_5', 'pm10')
    search_fields = ('station_name', 'station_id')

@admin.register(AtmosphericData)
class AtmosphericDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'latitude', 'longitude', 'temperature')
    list_filter = ('source',)

@admin.register(PredictedPM)
class PredictedPMAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'latitude', 'longitude', 'pm2_5_predicted')
    list_filter = ('timestamp',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ('name',)