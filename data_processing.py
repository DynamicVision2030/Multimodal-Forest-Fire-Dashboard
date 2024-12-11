import requests
import pandas as pd
import config  # Ensure your OpenWeatherMap API key is in config.py
import pandas as pd
import requests
import config

OPENWEATHERMAP_API_KEY = '07aedeaf81ff3057ec2adaaf5808b703'

def get_historical_data(lat, lon):
    # Assuming this is a function to fetch historical data from an API like OpenWeatherMap
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={config.API_KEY}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Parse the forecast data to extract temperature and humidity
        forecast_data = {
            'Time': [item['dt_txt'] for item in data['list']],
            'Temperature': [item['main']['temp'] for item in data['list']],
            'Humidity': [item['main']['humidity'] for item in data['list']]
        }
        df = pd.DataFrame(forecast_data)
        df['Time'] = pd.to_datetime(df['Time'])  # Convert Time column to datetime
        return df
    except requests.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if an error occurs


# Fetch current weather data from OpenWeatherMap
def fetch_weather_data(lat, lon):
    api_key = config.OPENWEATHERMAP_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Fetch forecast data from OpenWeatherMap (if needed)
def fetch_forecast_data(lat, lon):
    api_key = config.OPENWEATHERMAP_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Simulated function for checking battery status
def check_battery_status(node_name):
    return 75  # Example battery percentage



# Example function to identify high-risk nodes based on a threshold temperature
def get_high_risk_nodes(threshold_temp=20):
    high_risk_nodes = []
    for node_name, coordinates in config.NODES.items():
        lat, lon = coordinates["lat"], coordinates["lon"]
        
        # Assuming fetch_weather_data returns current weather data for the node
        node_weather = fetch_weather_data(lat, lon)

        # Check if temperature exceeds the threshold to mark as high risk
        if node_weather and node_weather['main']['temp'] >= threshold_temp:
            high_risk_nodes.append(node_name)
            
    return high_risk_nodes

