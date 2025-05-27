import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
user = "postgres"
password = "Papajohn.1234"  # Replace this
host = "localhost"
port = "5432"
database = "weather_data"

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
df = pd.read_sql("SELECT * FROM weather_hourly", engine)

# Parse timestamp column as datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Streamlit page setup
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("📊 Weather Dashboard - Helsinki")
st.write("Hourly data from Open-Meteo API")

# Sidebar filters
st.sidebar.header("📅 Filter by Date Range")
start_date = df["timestamp"].min().date()
end_date = df["timestamp"].max().date()
date_range = st.sidebar.slider("Select Date Range", start_date, end_date, (start_date, end_date))

filtered_df = df[(df["timestamp"].dt.date >= date_range[0]) & (df["timestamp"].dt.date <= date_range[1])]

st.sidebar.header("📊 Choose Metrics")
show_temp = st.sidebar.checkbox("Show Temperature", value=True)
show_humidity = st.sidebar.checkbox("Show Humidity", value=True)
show_wind = st.sidebar.checkbox("Show Wind Speed", value=True)

metrics = []
if show_temp:
    metrics.append("temperature")
if show_humidity:
    metrics.append("humidity")
if show_wind:
    metrics.append("wind_speed")

# Stats summary
st.subheader("Summary Statistics")
st.dataframe(filtered_df[metrics].describe().T.style.format(precision=2))

# Chart
st.subheader("Weather Trends")
if metrics:
    st.line_chart(filtered_df.set_index("timestamp")[metrics])
else:
    st.info("Please select at least one metric to display.")

# Raw data toggle
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)