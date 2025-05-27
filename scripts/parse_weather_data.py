import json
import pandas as pd
import os

def load_latest_weather_file():
    files = [f for f in os.listdir("data") if f.startswith("weather_") and f.endswith(".json")]
    files.sort(reverse=True)
    latest_file = os.path.join("data", files[0])
    with open(latest_file, "r") as f:
        data = json.load(f)
    return data

def parse_weather_data(data):
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    humidity = data["hourly"]["relative_humidity_2m"]
    wind = data["hourly"]["wind_speed_10m"]

    df = pd.DataFrame({
        "timestamp": times,
        "temperature": temps,
        "humidity": humidity,
        "wind_speed": wind
    })

    return df

if __name__ == "__main__":
    weather_json = load_latest_weather_file()
    df_weather = parse_weather_data(weather_json)
    print(df_weather.head())
