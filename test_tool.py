""" To test individual functions in command line tool (tool.py) """

import unittest
from unittest.mock import patch, mock_open
import json
import requests
from tool import prompt_user, load_serial_numbers, create_camera_config, configure_cameras

class TestTool(unittest.TestCase):

    # to verify user prompt
    @patch('builtins.input', side_effect=['TYPE_A', 'serial_numbers.json'])
    @patch('os.path.isfile', return_value=True)
    def test_prompt_user(self, mock_isfile, mock_input):
        camera_type, json_file_path = prompt_user()
        self.assertEqual(camera_type, 'TYPE_A')
        self.assertEqual(json_file_path, 'serial_numbers.json')

    # to verify correct loading and returning of serial numbers
    @patch('builtins.open', new_callable=mock_open, read_data='{"A": "DA2352466", "B": "DA2352453"}')
    def test_load_serial_numbers(self, mock_file):
        json_file_path = 'serial_numbers.json'
        serial_numbers = load_serial_numbers(json_file_path)
        expected_serial_numbers = {"A": "DA2352466", "B": "DA2352453"}
        self.assertEqual(serial_numbers, expected_serial_numbers)

    # to verify the list is correctly generated
    def test_create_camera_config(self):
        camera_type = 'TYPE_A'
        serial_numbers = {"A": "DA2352466", "B": "DA2352453"}
        camera_config = create_camera_config(camera_type, serial_numbers)
        expected_config = [
            {"ID": "A", "Serial": "DA2352466", "Type": "TYPE_A", "Gain": 20.0},
            {"ID": "B", "Serial": "DA2352453", "Type": "TYPE_A", "Gain": 20.0}
        ]
        self.assertEqual(camera_config, expected_config)

    # to verify appropiate message by simulating successful API response
    @patch('requests.put')
    def test_configure_cameras_success(self, mock_put):
        camera_config = [
            {"ID": "A", "Serial": "DA2352466", "Type": "TYPE_A", "Gain": 20.0},
            {"ID": "B", "Serial": "DA2352453", "Type": "TYPE_A", "Gain": 20.0}
        ]
        mock_put.return_value.status_code = 204
        with patch('builtins.print') as mock_print:
            configure_cameras(camera_config)
            mock_print.assert_called_with("Camera configuration successful.")

    # to verify appropiate message by simulating failed API response
    @patch('requests.put')
    def test_configure_cameras_failure(self, mock_put):
        camera_config = [
            {"ID": "A", "Serial": "DA2352466", "Type": "TYPE_A", "Gain": 20.0},
            {"ID": "B", "Serial": "DA2352453", "Type": "TYPE_A", "Gain": 20.0}
        ]
        mock_put.return_value.status_code = 400
        mock_put.return_value.text = "Invalid request."
        with patch('builtins.print') as mock_print:
            configure_cameras(camera_config)
            mock_print.assert_any_call("Failed to configure cameras. Status code: 400")
            mock_print.assert_any_call("Response:", "Invalid request.")

if __name__ == "__main__":
    unittest.main()

