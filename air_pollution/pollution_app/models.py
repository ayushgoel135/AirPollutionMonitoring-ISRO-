from django.db import models

class SatelliteData(models.Model):
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    aod_value = models.FloatField()
    satellite_source = models.CharField(max_length=50)
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['latitude', 'longitude']),
        ]

class GroundMeasurement(models.Model):
    station_id = models.CharField(max_length=50)
    station_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    pm2_5 = models.FloatField(null=True, blank=True)
    pm10 = models.FloatField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['station_id']),
        ]

class AtmosphericData(models.Model):
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    pressure = models.FloatField()
    source = models.CharField(max_length=50)
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['latitude', 'longitude']),
        ]

class PredictedPM(models.Model):
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    pm2_5_predicted = models.FloatField()
    pm10_predicted = models.FloatField()
    confidence_score = models.FloatField()
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['latitude', 'longitude']),
        ]

class State(models.Model):
    name = models.CharField(max_length=100)
    geojson_data = models.TextField()
    
    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    geojson_data = models.TextField()
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"