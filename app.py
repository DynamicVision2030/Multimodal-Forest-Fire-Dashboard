import streamlit as st
import folium
import plotly.graph_objects as go
from streamlit_folium import st_folium
from api_requests import fetch_weather_data, fetch_air_quality_data
from data_processing import get_historical_data, check_battery_status
from ui_components import display_weather_data, display_air_quality, display_alerts, display_historical_chart, display_battery_status
from utils import add_custom_css
from forecast import predict_fire_risk  # Importing the forecast function
import config



# def load_dashboard_page():
    

#     # Custom CSS for lighter UI colors
#     st.markdown("""
#         <style>
#             .main { background-color: #f0f2f6; color: #333; }
#             .stMetric, .st-subheader, .css-1kyxreq, .css-1v0mbdj {
#                 background-color: #ffffff !important;
#                 border: 1px solid #e0e0e0;
#                 border-radius: 8px;
#                 padding: 10px;
#             }
#             .stButton>button { background-color: #4CAF50; color: white; width: 100%; }
#             h1 { color: #4CAF50; }
#             h2, h3, h4 { color: #4CAF50; }
#             /* Center content */
#             .center-container { margin-left: auto; margin-right: auto; max-width: 90%; }
#         </style>
#     """, unsafe_allow_html=True)

#     # Dashboard Title
#     st.title("🌲 Forest Guard System Dashboard")

#     # Layout with two columns: left for map, right for scatter plot
#     col1, col2 = st.columns([1.2, 1])  # Adjust column ratios if needed

#     # Initialize session state to keep track of the selected node
#     if "selected_node" not in st.session_state:
#         st.session_state.selected_node = None

#     # Main Interactive Map on the Left
#     with col1:
#         st.subheader("🗺️ Node Map with Temperature-Based Colors")
#         map_center = [15.8700, 100.9925]  # Centered approximately on Thailand
#         m = folium.Map(location=map_center, zoom_start=6)

#         # Function to get marker color based on temperature
#         def get_marker_color(temperature):
#             if temperature < 23:
#                 return "blue"  # Cool
#             elif 23 <= temperature < 27:
#                 return "green"  # Mild
#             elif 27 <= temperature < 30:
#                 return "orange"  # Warm
#             else:
#                 return "red"  # Hot

#         # Add markers for each node with color based on temperature
#         for node_name, coordinates in config.NODES.items():
#             node_lat, node_lon = coordinates["lat"], coordinates["lon"]
#             node_weather = fetch_weather_data(node_lat, node_lon)
#             if node_weather:
#                 temperature = node_weather['main']['temp']
#                 marker_color = get_marker_color(temperature)
#                 icon_size = (35, 35) if node_name == st.session_state.selected_node else (20, 20)  # Larger icon for selected node
#                 folium.Marker(
#                     location=(node_lat, node_lon),
#                     popup=f"{node_name}: {temperature}°C",
#                     icon=folium.Icon(color=marker_color, icon_size=icon_size)
#                 ).add_to(m)
#             else:
#                 folium.Marker(
#                     location=(node_lat, node_lon),
#                     popup=f"{node_name}: Data Unavailable",
#                     icon=folium.Icon(color="gray", icon_size=(20, 20))
#                 ).add_to(m)

#         # Display the map
#         st_folium(m, width=1000, height=600)

#     # Scatter Plot on the Right
#     with col2:
#         st.subheader("📊 Multimodal Wildfire Forecasting")

#         # Prepare data for the scatter plot
#         latitudes = []
#         longitudes = []
#         colors = []
#         sizes = []  # Define sizes for each node
#         names = []

#         for node_name, coordinates in config.NODES.items():
#             lon = coordinates["lat"]
#             lat = coordinates["lon"]
#             fire_risk = predict_fire_risk(node_name)  # Prediction function from forecast.py
#             color = "red" if fire_risk == 1 else "green"  # Red for fire risk, green for no fire
#             latitudes.append(lat)
#             longitudes.append(lon)
#             colors.append(color)
#             sizes.append(20 if node_name != st.session_state.selected_node else 40)  # Larger size for selected node
#             names.append(node_name)

#         # Create scatter plot with hover info for names
#         scatter_fig = go.Figure(data=go.Scatter(
#             x=latitudes,
#             y=longitudes,
#             mode='markers',
#             marker=dict(color=colors, size=sizes),
#             text=names,  # Hover information with node names
#             hoverinfo="text"
#         ))

#         ## Update layout for the scatter plot with dotted gray gridlines
#         scatter_fig.update_layout(
#         title="Multimodal Wildfire Forecasting",
#         xaxis_title="Latitude",
#         yaxis_title="Longitude",
#         xaxis=dict(
#             range=[min(latitudes) - 0.5, max(latitudes) + 0.5],
#             showgrid=True,
#             gridcolor="gray",
#             gridwidth=0.5,
#             griddash="dot"  # Dotted gridlines for x-axis
#         ),
#         yaxis=dict(
#             range=[min(longitudes) - 0.5, max(longitudes) + 0.5],
#             showgrid=True,
#             gridcolor="gray",
#             gridwidth=0.5,
#             griddash="dot"  # Dotted gridlines for y-axis
#         ),
#         paper_bgcolor="white",
#         plot_bgcolor="white",
#         showlegend=False,
#         width=1000,  # Set your custom width here
#         height=600  # Set your custom height here
#     )


#         # Display scatter plot
#         st.plotly_chart(scatter_fig, use_container_width=True)

#     # 2x5 Grid of Buttons for Node Selection
#     st.subheader("🌍 Select a Node for Detailed Data")
#     node_names = list(config.NODES.keys())
#     cols = st.columns(5)

#     # Display buttons in a 2x5 grid layout
#     for idx, node_name in enumerate(node_names):
#         with cols[idx % 5]:  # Loop over columns to place buttons in grid
#             if st.button(node_name):
#                 st.session_state.selected_node = node_name  # Set selected node in session state

#     # Check if a node has been selected
#     if st.session_state.selected_node:
#         # Display data for the selected node
#         node_name = st.session_state.selected_node
#         node_coordinates = config.NODES[node_name]
#         lat, lon = node_coordinates["lat"], node_coordinates["lon"]

#         # Show the selected node details
#         st.subheader(f"📍 Detailed Data for {node_name}")

#         # Fetch and display weather data for the selected node
#         weather_data = fetch_weather_data(lat, lon)
#         if weather_data:
#             display_weather_data(weather_data)
#         else:
#             st.warning("Weather data unavailable.")

#         # Fetch and display air quality data for the selected node
#         aqi_data = fetch_air_quality_data(lat, lon)
#         if aqi_data:
#             display_air_quality(aqi_data)
#         else:
#             st.warning("Air quality data unavailable.")

#         # Display historical data charts for temperature and humidity
#         st.subheader(f"📈 Historical Temperature and Humidity Data for {node_name}")
#         historical_data = get_historical_data(node_name)
#         display_historical_chart(historical_data)

#         # Display battery status for the selected node
#         st.subheader(f"🔋 Battery Status for {node_name}")
#         battery_status = check_battery_status(node_name)
#         display_battery_status(battery_status)

#         # Display alerts based on conditions
#         st.subheader("🚨 Alerts")
#         display_alerts(weather_data, aqi_data, battery_status)
#     else:
#         st.info("Please select a node to view its detailed data.")
# load_dashboard_page function

def load_dashboard_page():
    # Custom CSS for lighter UI colors
    st.markdown("""
        <style>
            .main { background-color: #f0f2f6; color: #333; }
            .stMetric, .st-subheader, .css-1kyxreq, .css-1v0mbdj {
                background-color: #ffffff !important;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
            .stButton>button { background-color: #4CAF50; color: white; width: 100%; }
            h1 { color: #4CAF50; }
            h2, h3, h4 { color: #4CAF50; }
            /* Center content */
            .center-container { margin-left: auto; margin-right: auto; max-width: 90%; }
        </style>
    """, unsafe_allow_html=True)

    # Dashboard Title
    st.title("🌲 Forest Guard System Dashboard")

    # Layout with two columns: left for map, right for scatter plot
    col1, col2 = st.columns([1.2, 1])  # Adjust column ratios if needed

    # Initialize session state to keep track of the selected node
    if "selected_node" not in st.session_state:
        st.session_state.selected_node = None

    # Main Interactive Map on the Left
    with col1:
        st.subheader("🗺️ Node Map with Temperature-Based Colors")
        map_center = [15.8700, 100.9925]  # Centered approximately on Thailand
        m = folium.Map(location=map_center, zoom_start=6)

        # Function to get marker color based on temperature
        def get_marker_color(temperature):
            if temperature < 23:
                return "blue"  # Cool
            elif 23 <= temperature < 27:
                return "green"  # Mild
            elif 27 <= temperature < 30:
                return "orange"  # Warm
            else:
                return "red"  # Hot

        # Add markers for each node with color based on temperature
        for node_name, coordinates in config.NODES.items():
            node_lat, node_lon = coordinates["lat"], coordinates["lon"]
            node_weather = fetch_weather_data(node_lat, node_lon)
            if node_weather:
                temperature = node_weather['main']['temp']
                marker_color = get_marker_color(temperature)
                icon_size = (35, 35) if node_name == st.session_state.selected_node else (20, 20)  # Larger icon for selected node
                folium.Marker(
                    location=(node_lat, node_lon),
                    popup=f"{node_name}: {temperature}°C",
                    icon=folium.Icon(color=marker_color, icon_size=icon_size)
                ).add_to(m)
            else:
                folium.Marker(
                    location=(node_lat, node_lon),
                    popup=f"{node_name}: Data Unavailable",
                    icon=folium.Icon(color="gray", icon_size=(20, 20))
                ).add_to(m)

        # Display the map
        st_folium(m, width=1000, height=600)

    # Scatter Plot on the Right
    with col2:
        st.subheader("📊 Multimodal Wildfire Forecasting")

        # Prepare data for the scatter plot
        latitudes = []
        longitudes = []
        colors = []
        sizes = []  # Define sizes for each node
        names = []

        for node_name, coordinates in config.NODES.items():
            lon = coordinates["lat"]
            lat = coordinates["lon"]
            fire_risk = predict_fire_risk(node_name)  # Prediction function from forecast.py
            color = "red" if fire_risk == 1 else "green"  # Red for fire risk, green for no fire
            latitudes.append(lat)
            longitudes.append(lon)
            colors.append(color)
            sizes.append(20 if node_name != st.session_state.selected_node else 40)  # Larger size for selected node
            names.append(node_name)

        # Create scatter plot with hover info for names
        scatter_fig = go.Figure(data=go.Scatter(
            x=latitudes,
            y=longitudes,
            mode='markers',
            marker=dict(color=colors, size=sizes),
            text=names,  # Hover information with node names
            hoverinfo="text"
        ))

        scatter_fig.update_layout(
            title="Multimodal Wildfire Forecasting",
            xaxis_title="Latitude",
            yaxis_title="Longitude",
            xaxis=dict(
                range=[min(latitudes) - 0.5, max(latitudes) + 0.5],
                showgrid=True,
                gridcolor="gray",
                gridwidth=0.5,
                griddash="dot"
            ),
            yaxis=dict(
                range=[min(longitudes) - 0.5, max(longitudes) + 0.5],
                showgrid=True,
                gridcolor="gray",
                gridwidth=0.5,
                griddash="dot"
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False,
            width=1000,
            height=600
        )

        # Display scatter plot
        st.plotly_chart(scatter_fig, use_container_width=True)

    # Node selection buttons and detailed data display
    st.subheader("🌍 Select a Node for Detailed Data")
    node_names = list(config.NODES.keys())
    cols = st.columns(5)

    # Display buttons in a 2x5 grid layout
    for idx, node_name in enumerate(node_names):
        with cols[idx % 5]:  # Loop over columns to place buttons in grid
            if st.button(node_name):
                st.session_state.selected_node = node_name  # Set selected node in session state

    # Check if a node has been selected
    if st.session_state.selected_node:
        # Display data for the selected node
        node_name = st.session_state.selected_node
        node_coordinates = config.NODES[node_name]
        lat, lon = node_coordinates["lat"], node_coordinates["lon"]

        # Show the selected node details
        st.subheader(f"📍 Detailed Data for {node_name}")

        # Fetch and display weather data for the selected node
        weather_data = fetch_weather_data(lat, lon)
        if weather_data:
            display_weather_data(weather_data)
        else:
            st.warning("Weather data unavailable.")

        # Fetch and display air quality data for the selected node
        aqi_data = fetch_air_quality_data(lat, lon)
        if aqi_data:
            display_air_quality(aqi_data)
        else:
            st.warning("Air quality data unavailable.")

        # Display historical and forecast data charts for temperature and humidity
        st.subheader(f"📈 Historical and Forecast Temperature and Humidity Data for {node_name}")
        historical_data = get_historical_data(lat, lon)
        display_historical_chart(lat, lon, historical_data)

        # Display battery status for the selected node
        st.subheader(f"🔋 Battery Status for {node_name}")
        battery_status = check_battery_status(node_name)
        display_battery_status(battery_status)

        # Display alerts based on conditions
        st.subheader("🚨 Alerts")
        display_alerts(weather_data, aqi_data, battery_status)
    else:
        st.info("Please select a node to view its detailed data.")


