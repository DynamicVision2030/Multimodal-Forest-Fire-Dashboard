import streamlit as st

# Custom CSS to style Streamlit components
def add_custom_css():
    st.markdown("""
        <style>
            .main {
                background-color: #2f3136;
                color: #ffffff;
            }
            .stMetric {
                background-color: #333;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
                color: #FFFFFF;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)


def convert_to_binary(data):
    """
    Converts a list of dictionaries to a binary string for transmission.
    Each dictionary in the list represents a node with key-value pairs.
    """
    binary_string = ""
    for node in data:  # Loop through each dictionary in the list
        for key, value in node.items():
            # Convert each key and value to binary
            key_binary = ''.join(format(ord(char), '08b') for char in key)
            value_binary = ''.join(format(ord(char), '08b') for char in str(value))
            binary_string += key_binary + value_binary
    return binary_string
