import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    print("Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_successful_prediction():
    print("Testing Successful Prediction (High Traffic)...")
    payload = {
        "vehicle_count_north": 45,
        "vehicle_count_south": 50,
        "vehicle_count_east": 42,
        "vehicle_count_west": 48,
        "pedestrian_count": 12,
        "emergency_vehicle": 0,
        "time_of_day": "Evening",
        "weather_condition": "Rainy"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_validation_error():
    print("Testing API Data Validation (Sending invalid string instead of int)...")
    # Sending 'LOTS' instead of an integer for north vehicle count
    bad_payload = {
        "vehicle_count_north": "LOTS", 
        "vehicle_count_south": 10,
        "vehicle_count_east": 12,
        "vehicle_count_west": 11,
        "pedestrian_count": 2,
        "emergency_vehicle": 0,
        "time_of_day": "Morning",
        "weather_condition": "Sunny"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=bad_payload)
    print(f"Status Code: {response.status_code} (Expected 422 Unprocessable Entity)")
    print(f"Response Error Details: {response.json()['detail'][0]['msg']}\n")

if __name__ == "__main__":
    try:
        test_health_check()
        test_successful_prediction()
        test_validation_error()
    except requests.exceptions.ConnectionError:
        print("ERROR: Looks like your API server isn't running. Start app.py first!")