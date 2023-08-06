import unittest
from unittest.mock import patch
import requests

# To run all tests in this folder use the following command:
# python -m unittest discover -s tests

from mlb_data.mlb_data_ingest.MLBDataIngestor import MLBDataIngestor


class TestMLBDataIngestor(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = MLBDataIngestor()
        self.endpoint = "teams"

    @patch.object(requests, "get")
    def test_successful_api_call(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"teams": [{"id": 1, "name": "team1"}, {"id": 2, "name": "team2"}]}

        data = self.data_ingestor.call_api(self.endpoint)

        self.assertIsNotNone(data)
        self.assertEqual(data, {"teams": [{"id": 1, "name": "team1"}, {"id": 2, "name": "team2"}]})
        mock_get.assert_called_once_with(
            f"{self.data_ingestor.BASE_URL}/{self.data_ingestor.VERSION}/{self.endpoint}", params=None, timeout=10
        )


if __name__ == "__main__":
    unittest.main()
