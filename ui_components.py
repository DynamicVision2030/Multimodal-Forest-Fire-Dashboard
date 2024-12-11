import streamlit as st
import plotly.graph_objects as go
from api_requests import fetch_weather_data, fetch_air_quality_data  # Updated import
from data_processing import fetch_forecast_data, fetch_weather_data
import pandas as pd

# Function to display air quality data
def display_air_quality(aqi_data):
    st.subheader("🌬️ Air Quality Index")
    aqi = aqi_data['list'][0]['main']['aqi']
    co = aqi_data['list'][0]['components']['co']
    no2 = aqi_data['list'][0]['components']['no2']
    o3 = aqi_data['list'][0]['components']['o3']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("AQI Level", aqi)
    col2.metric("CO (μg/m³)", co)
    col3.metric("NO₂ (μg/m³)", no2)

# Existing functions from your code
def display_historical_chart(lat, lon, data):
    data = fetch_forecast_data(lat, lon)
    
    if data:
        forecast_data = {
            'Time': [item['dt_txt'] for item in data['list']],
            'Temperature': [item['main']['temp'] for item in data['list']],
            'Humidity': [item['main']['humidity'] for item in data['list']]
        }
        df = pd.DataFrame(forecast_data)
        df['Time'] = pd.to_datetime(df['Time'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df['Temperature'], 
            name="Temperature (°C)", 
            line=dict(color='#FF5733', width=2),
            yaxis="y1"
        ))
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df['Humidity'], 
            name="Humidity (%)", 
            line=dict(color='#3498DB', width=2, dash='dash'),
            yaxis="y2"
        ))

        fig.update_layout(
            title='Forecast Temperature and Humidity Data',
            xaxis=dict(title="Time"),
            yaxis=dict(
                title="Temperature (°C)", 
                titlefont=dict(color="#FF5733"), 
                tickfont=dict(color="#FF5733"),
            ),
            yaxis2=dict(
                title="Humidity (%)",
                titlefont=dict(color="#3498DB"),
                tickfont=dict(color="#3498DB"),
                overlaying="y",
                side="right"
            ),
            plot_bgcolor="#f9f9f9",
            paper_bgcolor="#f0f2f6",
            font=dict(color="#333"),
            title_font=dict(color="#333"),
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
            margin=dict(l=0, r=0, t=40, b=0),
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Forecast data unavailable.")

def display_weather_data(weather_data):
    st.subheader("🌡️ Weather Data")
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    wind_deg = weather_data['wind']['deg']

    wind_direction = get_wind_direction_symbol(wind_deg)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Temperature (°C)", f"{temp}°", delta=f"Feels like {feels_like}°")
    col2.metric("Humidity (%)", f"{humidity}%")
    col3.metric("Wind Speed (m/s)", f"{wind_speed} m/s")
    col4.metric("Wind Degree (°)", f"{wind_deg} °")
    col5.metric("Wind Direction", f"{wind_direction}")

def get_wind_direction_symbol(deg):
    directions = ["↑ North", "↗ NE", "→ East", "↘ SE", "↓ South", "↙ SW", "← West", "↖ NW"]
    return directions[int((deg % 360) / 45)]

def display_battery_status(battery_status):
    st.subheader("Battery Status")
    color = "green" if battery_status >= 50 else "orange" if battery_status >= 20 else "red"
    st.metric(label="Battery Status", value=f"{battery_status}%", delta="Stable", help="Battery status for the selected node.")


import streamlit as st

# Function to display alerts based on conditions
def display_alerts(weather_data, aqi_data, battery_status):
    st.subheader("🚨 Alerts")

    # Get the temperature and air quality index
    temperature = weather_data['main']['temp']
    aqi = aqi_data['list'][0]['main']['aqi']

    # Check for high temperature alert
    if temperature > 35:
        st.warning("🔥 High temperature alert! Risk of fire ignition is elevated.")

    # Check for poor air quality alert
    if aqi > 100:
        st.warning("⚠️ Air Quality Alert: Poor air quality detected.")

    # Check for low battery alert
    if battery_status < 20:
        st.warning("⚠️ Battery Low: Node battery is below 20% and may need replacement soon.")
