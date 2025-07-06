from django.test import TestCase
from django.urls import reverse
from .models import State

class ModelTests(TestCase):
    def test_state_creation(self):
        state = State.objects.create(
            name="Test State",
            geojson_data='{"type": "FeatureCollection", "features": []}'
        )
        self.assertEqual(str(state), "Test State")

class ViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Air Pollution Monitoring")