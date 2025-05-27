import requests
import json
from datetime import datetime

def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 60.1699,  # Helsinki
        "longitude": 24.9384,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Europe/Helsinki"
    }

    response = requests.get(url, params=params)
    data = response.json()

    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"data/weather_{now}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Weather data saved to {filename}")

if __name__ == "__main__":
    fetch_weather_data()
