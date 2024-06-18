import json
import requests
import os

# prompt user to input camera type and JSON file path
def prompt_user():
    camera_type = input("Enter camera type (TYPE_A or TYPE_B): ").strip().upper()
    while camera_type not in ['TYPE_A', 'TYPE_B']:
        print("Invalid camera type. Please enter either 'TYPE_A' or 'TYPE_B'.")
        camera_type = input("Enter camera type (TYPE_A or TYPE_B): ").strip().upper()

    json_file_path = input("Enter path to the JSON file containing serial numbers: ").strip()
    while not os.path.isfile(json_file_path):
        print("Invalid file path. Please enter a valid path to the JSON file.")
        json_file_path = input("Enter path to the JSON file containing serial numbers: ").strip()

    return camera_type, json_file_path

# loading serial numbers from the JSON file
def load_serial_numbers(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

# creating a list of configuration dictionaries
def create_camera_config(camera_type, serial_numbers):
    camera_config = []
    gain_value = 20.0

    for id, serial in serial_numbers.items():
        config = {
            "ID": id,
            "Serial": serial,
            "Type": camera_type,
            "Gain": gain_value
        }
        camera_config.append(config)
    
    return camera_config

# sending configuration to the API by PUT request
def configure_cameras(camera_config):
    url = "http://localhost:8888/api/v1/config/cameras"
    headers = {'Content-Type': 'application/json'}

    response = requests.put(url, headers=headers, data=json.dumps(camera_config))

    # validating data
    if response.status_code == 204:
        print("Camera configuration successful.")
    else:
        # indicates potential issue
        print(f"Failed to configure cameras. Status code: {response.status_code}")
        print("Response:", response.text)

# main function
def main():
    camera_type, json_file_path = prompt_user()
    serial_numbers = load_serial_numbers(json_file_path)
    camera_config = create_camera_config(camera_type, serial_numbers)
    configure_cameras(camera_config)

if __name__ == "__main__":
    main()

