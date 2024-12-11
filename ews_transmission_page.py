import streamlit as st
import config
from data_processing import get_high_risk_nodes
from utils import convert_to_binary

# Custom CSS for enhanced styling
st.markdown("""
    <style>
        .main { background-color: #f9fafc; color: #333; }
        .stMetric, .st-subheader, .css-1kyxreq, .css-1v0mbdj {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton>button { background-color: #ff6b6b; color: white; font-size: 16px; padding: 12px; width: 100%; border-radius: 8px; }
        h1, h2 { color: #4CAF50; }
        .high-risk-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .metric-badge {
            font-size: 1.1em;
            color: #4CAF50;
            background-color: #e0f7e9;
            padding: 5px 10px;
            border-radius: 5px;
            margin: 5px 0;
            display: inline-block;
        }
        .binary-box {
            font-family: monospace;
            background-color: #e0f7e9;
            padding: 10px;
            border-radius: 5px;
            color: #333;
            overflow-wrap: break-word;
            margin-top: 10px;
        }
        .metric-icon {
            color: #ff6b6b;
            font-size: 1.2em;
            margin-right: 5px;
            vertical-align: middle;
        }
        .alert-header { color: #ff6b6b; }
    </style>
""", unsafe_allow_html=True)

def load_ews_transmission_page():
    st.title("🚨 Early Warning System (EWS) Transmission")
    
    # Summary section
    st.subheader("Summary")
    high_risk_count = len(st.session_state.high_risk_nodes) if "high_risk_nodes" in st.session_state else 0
    st.metric("High-Risk Nodes", high_risk_count)

    if high_risk_count > 0:
        st.subheader("📍 High-Risk Nodes Ready for Transmission")
        
        for node in st.session_state.high_risk_nodes:
            # Display each node's information in a styled card
            st.markdown(f"""
                <div class="high-risk-card">
                    <h4 class="alert-header">🔥 {node['name']}</h4>
                    <div><strong>Location:</strong> ({node['lat']}, {node['lon']})</div>
                    <div><span class="metric-icon">🌡️</span> <span class="metric-badge">Temperature: {node['temperature']}°C</span></div>
                    <div><span class="metric-icon">💧</span> <span class="metric-badge">Humidity: {node['humidity']}%</span></div>
                    <div><span class="metric-icon">🔥</span> <span class="metric-badge">Fire Risk Confidence: {node['fire_risk']:.2f}</span></div>
                </div>
            """, unsafe_allow_html=True)
        
        # Transmission button with binary display
        if st.button("🚀 Transmit Alerts and Clear Queue"):
            with st.spinner("Transmitting alerts..."):
                # Convert data to binary format for transmission
                binary_data = convert_to_binary(st.session_state.high_risk_nodes)
                response = simulate_transmission(binary_data, satellite_band="L1", recipients=["Authorities", "Local Communities"])
                
                if response["status"] == "success":
                    st.session_state.high_risk_nodes.clear()
                    st.success(f"Alerts transmitted successfully at {response['time']}. Queue cleared.")
                    
                    # Display binary data sent
                    st.subheader("📡 Binary Data Transmitted")
                    formatted_binary = " ".join(binary_data[i:i+8] for i in range(0, len(binary_data), 8))  # Group in bytes for readability
                    st.markdown(f"<div class='binary-box'>{formatted_binary}</div>", unsafe_allow_html=True)
                else:
                    st.error("Transmission failed. Please try again.")
    else:
        st.info("No high-risk nodes available for transmission.")

def simulate_transmission(binary_data, satellite_band, recipients):
    # Mock function to simulate transmission
    import time
    time.sleep(1)  # Simulate a delay
    return {"status": "success", "time": "2024-11-04 12:00 UTC"}
