# import streamlit as st
# # Page configuration
# st.set_page_config(page_title="Forest Guard System", layout="wide")
# from app import load_dashboard_page
# from detection_page import load_detection_page
# from page1 import load_page1
# from page2 import load_page2
# from page3 import load_page3
# from ews_transmission_page import load_ews_transmission_page  # Import EWS transmission page



# # Sidebar for page navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Dashboard", "Detection", "EWS Transmission", "Page 1", "Page 2", "Page 3"])

# # Load the selected page's content
# if page == "Dashboard":
#     load_dashboard_page()
# elif page == "Detection":
#     load_detection_page()
# elif page == "EWS Transmission":  # Add EWS transmission option
#     load_ews_transmission_page()
# elif page == "Page 1":
#     load_page1()
# elif page == "Page 2":
#     load_page2()
# elif page == "Page 3":
#     load_page3()

import streamlit as st
# Page configuration
st.set_page_config(page_title="Forest Guard System", layout="wide")
from app import load_dashboard_page
from detection_page import load_detection_page
from page1 import load_page1
from page2 import load_page2
from page3 import load_page3
from ews_transmission_page import load_ews_transmission_page  # Import EWS transmission page






# Logo display (ensure the file path is correct)
logo_path = "logo.png"  # Replace with the correct path to your logo image
st.sidebar.image(logo_path, width=250, use_column_width=False)  # Adjust width as needed

# Sidebar for page navigation
st.sidebar.title("Navigation")
#page = st.sidebar.radio("Go to", ["Dashboard", "Detection", "EWS Transmission", "Page 1", "Page 2", "Page 3"])
page = st.sidebar.radio("Go to", ["Dashboard", "Detection", "EWS Transmission", "Page 1", "Page 2", "Page 3"])



if page == "Dashboard":
    load_dashboard_page()
elif page == "Detection":
    load_detection_page()
elif page == "EWS Transmission":  # Add EWS transmission option
    load_ews_transmission_page()
elif page == "Data Architecture":
    load_page1()
elif page == "Multimodal Architecture":
    load_page2()
elif page == "Page 3":
    load_page3()