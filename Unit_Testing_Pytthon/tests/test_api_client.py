import unittest
from src.api_client import get_location
from unittest.mock import patch, Mock

class ApiClientTests(unittest.TestCase):
    @patch("src.api_client.requests.get")
    def test_get_location_returns_expected_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            
        }
        result = get_location("8.8.8.8")
        self.assertEqual(
            result.get('country'), "United States of America"
        )