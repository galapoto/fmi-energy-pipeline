import pandas as pd
import json
import os
from sqlalchemy import create_engine

# Load the latest weather file
def load_latest_weather_file():
    files = [f for f in os.listdir("data") if f.startswith("weather_") and f.endswith(".json")]
    files.sort(reverse=True)
    latest_file = os.path.join("data", files[0])
    with open(latest_file, "r") as f:
        data = json.load(f)
    return data

# Parse JSON into DataFrame
def parse_weather_data(data):
    df = pd.DataFrame({
        "timestamp": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
        "wind_speed": data["hourly"]["wind_speed_10m"]
    })
    return df

# Save DataFrame to PostgreSQL
def save_to_postgres(df):
    # Replace these with your actual PostgreSQL connection details
    user = "postgres"
    password = "Papajohn.1234"
    host = "localhost"
    port = "5432"
    database = "weather_data"

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    df.to_sql("weather_hourly", engine, if_exists="replace", index=False)
    print("✅ Data saved to PostgreSQL table: weather_hourly")

if __name__ == "__main__":
    raw_data = load_latest_weather_file()
    df_weather = parse_weather_data(raw_data)
    save_to_postgres(df_weather)