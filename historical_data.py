import requests
import pandas as pd
import config  # Make sure your config file has the VISUAL_CROSSING_API_KEY

def get_historical_data(lat, lon):
    api_key = config.VISUAL_CROSSING_API_KEY
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    url = f"{base_url}/{lat},{lon}/last30days"
    
    params = {
        "unitGroup": "metric",
        "key": api_key,
        "contentType": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        # Parse data into a DataFrame
        records = [
            {
                'Time': day['datetime'],
                'Temperature': day.get('temp', None),
                'Humidity': day.get('humidity', None)
            }
            for day in data['days']
        ]

        df = pd.DataFrame(records)
        df['Time'] = pd.to_datetime(df['Time'])  # Convert Time to datetime
        return df
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Test the function with a sample location (latitude and longitude)
latitude = 18.7883   # Example: Chiang Mai
longitude = 98.9853

df = get_historical_data(latitude, longitude)
if df is not None:
    print("Data retrieved successfully:")
    print(df.head())  # Display the first few rows
else:
    print("Failed to retrieve data.")
