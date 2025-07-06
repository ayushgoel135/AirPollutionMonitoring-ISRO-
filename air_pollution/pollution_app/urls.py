from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/pollution-data/', views.get_pollution_data, name='pollution_data'),
    path('api/geojson-data/', views.get_geojson_data, name='geojson_data'),
    path('api/pm-predictions/', views.get_pm_predictions, name='pm_predictions'),
]
