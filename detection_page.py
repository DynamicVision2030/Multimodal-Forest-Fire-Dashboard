# import streamlit as st
# import numpy as np
# from PIL import Image
# import onnxruntime as ort

# # Load the ONNX model
# MODEL_PATH = "model.onnx"
# session = ort.InferenceSession(MODEL_PATH)

# def preprocess_image(image, target_shape):
#     """Resize and normalize the image for the model."""
#     image = image.resize(target_shape)
#     image = np.array(image) / 255.0  # Normalize to [0, 1]
#     if len(image.shape) == 2:  # Grayscale
#         image = np.expand_dims(image, axis=-1)
#     return np.transpose(image, (2, 0, 1)).astype(np.float32)  # Channels first

# def load_detection_page():
#     # Page title
#     st.title("🔥 Multimodal Wildfire Detection System")

#     # Instructions
#     st.markdown("### Upload your data below to predict wildfire risk.")
#     st.write("This page allows you to upload environmental data and images to simulate a prediction on wildfire risk using our multimodal model.")

#     # Layout setup: 2 columns
#     col1, col2 = st.columns([1, 1])

#     # Column 1: Data Inputs (Temperature, Humidity, Wind Speed, Wind Direction)
#     with col1:
#         st.subheader("📊 Environmental Data")

#         # Temperature Input
#         temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, value=25.0)

#         # Humidity Input
#         humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=50)

#         # Wind Speed Input
#         wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=100.0, value=5.0)

#         # Wind Direction Input
#         wind_direction = st.selectbox(
#             "Wind Direction",
#             options=["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
#         )

#     # Column 2: Upload Inputs (Fire/No Fire Image, Spectrogram)
#     with col2:
#         st.subheader("📷 Image & Spectrogram Data")

#         # Image Upload for Fire/No Fire
#         fire_image = st.file_uploader("Upload Fire/No Fire Image", type=["jpg", "jpeg", "png"])
#         if fire_image:
#             img = Image.open(fire_image)
#             st.image(img, caption="Uploaded Image", use_column_width=True)

#         # Spectrogram Upload
#         spectrogram = st.file_uploader("Upload Spectrogram Image", type=["jpg", "jpeg", "png"])
#         if spectrogram:
#             spec_img = Image.open(spectrogram)
#             st.image(spec_img, caption="Uploaded Spectrogram", use_column_width=True)

#     # Prediction Button
#     st.markdown("### 📈 Prediction")
#     if st.button("Run Wildfire Detection"):
#         # Preprocess inputs
#         inputs = {}
        
#         if fire_image:
#             # Preprocess fire image
#             processed_image = preprocess_image(img, (28, 28))  # Assuming Input shape (3, 28, 28)
#             inputs['Input'] = np.expand_dims(processed_image, axis=0)  # Add batch dimension

#         if spectrogram:
#             # Preprocess spectrogram
#             processed_spectrogram = preprocess_image(spec_img, (32, 32))  # Assuming Input_2 shape (1, 32, 32)
#             inputs['Input_2'] = np.expand_dims(processed_spectrogram, axis=0)  # Add batch dimension

#         # Prepare environmental data (Inputs 3 to 6)
#         # Assume they match the shape required for `Input_3` to `Input_6`
#         inputs['Input_3'] = np.array([[temperature]], dtype=np.float32)
#         inputs['Input_4'] = np.array([[humidity]], dtype=np.float32)
#         inputs['Input_5'] = np.array([[wind_speed]], dtype=np.float32)
#         # Convert wind direction to one-hot encoding or other format as needed for `Input_6`
#         wind_direction_mapping = {
#             "North": 0, "North-East": 1, "East": 2, "South-East": 3,
#             "South": 4, "South-West": 5, "West": 6, "North-West": 7
#         }
#         wind_direction_value = wind_direction_mapping[wind_direction]
#         inputs['Input_6'] = np.array([[wind_direction_value]], dtype=np.float32)

#         # Run inference
#         st.write("Running model prediction...")
#         outputs = session.run(None, inputs)
        
#         # Get result
#         result = outputs[0][0][0]  # Assuming binary output in first position
#         prediction = "Fire" if result > 0.5 else "No Fire"  # Threshold for binary classification
#         confidence = result if result > 0.5 else 1 - result  # Confidence for display

#         # Display result
#         st.subheader(f"🔥 Prediction Result: {prediction}")
#         st.write(f"Confidence: {confidence:.2f}")

#     # Add a note for users
#     st.info("Note: This demonstration uses a trained ONNX model for predictions.")
import streamlit as st
import numpy as np
from PIL import Image
import onnxruntime as ort

# Load the ONNX model
MODEL_PATH = "model.onnx"
session = ort.InferenceSession(MODEL_PATH)

# Custom CSS for a green-themed minimalist look
st.markdown("""
    <style>
        /* Set the main background color and font */
        .main { background-color: #f0f2f6; color: #333; }

        /* Sidebar style */
        .css-1y4p8pa { background-color: #ffffff; color: #333; }

        /* Title and header styles */
        h1, h2, h3, h4, .st-subheader { color: #4CAF50; }

        /* Input fields and buttons */
        .stNumberInput, .stSelectbox, .stFileUploader {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            color: #333;
        }

        /* Prediction button */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
            font-size: 16px;
        }

        /* Information and note box */
        .st-info { 
            background-color: #e0f7e9;
            color: #333;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }

        /* Image display styling */
        img { 
            border: 1px solid #ddd; 
            border-radius: 4px;
            padding: 5px;
        }
    </style>
# """, unsafe_allow_html=True)

# def preprocess_image(image, target_shape):
#     """Resize and normalize the image for the model."""
#     image = image.resize(target_shape)
#     image = np.array(image) / 255.0
#     if len(image.shape) == 2:
#         image = np.expand_dims(image, axis=-1)
#     return np.transpose(image, (2, 0, 1)).astype(np.float32)

# def load_detection_page():
#     st.title("🔥 Multimodal Wildfire Detection System")
#     st.markdown("Upload your data below to predict wildfire risk.")

#     # Layout setup
#     col1, col2 = st.columns([1, 1])

#     # Data inputs
#     with col1:
#         st.subheader("📊 Environmental Data")
#         temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, value=25.0)
#         humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=50)
#         wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=100.0, value=5.0)
#         wind_direction = st.selectbox("Wind Direction", options=["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"])

#     # Image and spectrogram data
#     with col2:
#         st.subheader("📷 Image & Spectrogram Data")
#         fire_image = st.file_uploader("Upload Fire/No Fire Image", type=["jpg", "jpeg", "png"])
#         if fire_image:
#             img = Image.open(fire_image)
#             st.image(img, caption="Uploaded Image", use_column_width=True)

#         spectrogram = st.file_uploader("Upload Spectrogram Image", type=["jpg", "jpeg", "png"])
#         if spectrogram:
#             spec_img = Image.open(spectrogram)
#             st.image(spec_img, caption="Uploaded Spectrogram", use_column_width=True)

#     # Prediction
#     st.markdown("### 📈 Prediction")
#     if st.button("Run Wildfire Detection"):
#         inputs = {}
#         if fire_image:
#             processed_image = preprocess_image(img, (28, 28))
#             inputs['Input'] = np.expand_dims(processed_image, axis=0)
#         if spectrogram:
#             processed_spectrogram = preprocess_image(spec_img, (32, 32))
#             inputs['Input_2'] = np.expand_dims(processed_spectrogram, axis=0)

#         inputs['Input_3'] = np.array([[temperature]], dtype=np.float32)
#         inputs['Input_4'] = np.array([[humidity]], dtype=np.float32)
#         inputs['Input_5'] = np.array([[wind_speed]], dtype=np.float32)
        
#         wind_mapping = {"North": 0, "North-East": 1, "East": 2, "South-East": 3, "South": 4, "South-West": 5, "West": 6, "North-West": 7}
#         inputs['Input_6'] = np.array([[wind_mapping[wind_direction]]], dtype=np.float32)

#         st.write("Running model prediction...")
#         outputs = session.run(None, inputs)
        
#         result = outputs[0][0][0]
#         prediction = "Fire" if result > 0.5 else "No Fire"
#         confidence = result if result > 0.5 else 1 - result

#         st.subheader(f"🔥 Prediction Result: {prediction}")
#         st.write(f"Confidence: {confidence:.2f}")

#     # Add a note for users
#     st.markdown("<div class='st-info'>Note: This demonstration uses a trained ONNX model for predictions.</div>", unsafe_allow_html=True)
import streamlit as st
import numpy as np
from PIL import Image
import onnxruntime as ort

# Load the ONNX model
MODEL_PATH = "model.onnx"
session = ort.InferenceSession(MODEL_PATH)

# Custom CSS for a green-themed minimalist look
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; color: #333; }
        .css-1y4p8pa { background-color: #ffffff; color: #333; }
        h1, h2, h3, h4, .st-subheader { color: #4CAF50; }
        .stNumberInput, .stSelectbox, .stFileUploader {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            color: #333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
            font-size: 16px;
        }
        .st-info { 
            background-color: #e0f7e9;
            color: #333;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }
        img { 
            border: 1px solid #ddd; 
            border-radius: 4px;
            padding: 5px;
        }
    </style>
""", unsafe_allow_html=True)

def preprocess_image(image, target_shape):
    """Resize and normalize the image for the model."""
    image = image.resize(target_shape)
    image = np.array(image) / 255.0
    if len(image.shape) == 2:
        image = np.expand_dims(image, axis=-1)
    return np.transpose(image, (2, 0, 1)).astype(np.float32)

def load_detection_page():
    st.title("🔥 Multimodal Wildfire Detection System")
    st.markdown("Upload your data below to predict wildfire risk.")

    # Layout setup
    col1, col2 = st.columns([1, 1])

    # Data inputs
    with col1:
        st.subheader("📊 Environmental Data")
        temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, value=25.0)
        humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=50)
        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=100.0, value=5.0)
        wind_direction = st.selectbox("Wind Direction", options=["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"])

    # Image and spectrogram data
    with col2:
        st.subheader("📷 Image & Spectrogram Data")
        fire_image = st.file_uploader("Upload Fire/No Fire Image", type=["jpg", "jpeg", "png"])
        if fire_image:
            img = Image.open(fire_image)
            st.image(img, caption="Uploaded Image", use_column_width=True)

        spectrogram = st.file_uploader("Upload Spectrogram Image", type=["jpg", "jpeg", "png"])
        if spectrogram:
            spec_img = Image.open(spectrogram)
            st.image(spec_img, caption="Uploaded Spectrogram", use_column_width=True)

    # Prediction
    st.markdown("### 📈 Prediction")
    if st.button("Run Wildfire Detection"):
        inputs = {}
        if fire_image:
            processed_image = preprocess_image(img, (28, 28))
            inputs['Input'] = np.expand_dims(processed_image, axis=0)
        if spectrogram:
            processed_spectrogram = preprocess_image(spec_img, (32, 32))
            inputs['Input_2'] = np.expand_dims(processed_spectrogram, axis=0)

        inputs['Input_3'] = np.array([[temperature]], dtype=np.float32)
        inputs['Input_4'] = np.array([[humidity]], dtype=np.float32)
        inputs['Input_5'] = np.array([[wind_speed]], dtype=np.float32)
        
        wind_mapping = {"North": 0, "North-East": 1, "East": 2, "South-East": 3, "South": 4, "South-West": 5, "West": 6, "North-West": 7}
        inputs['Input_6'] = np.array([[wind_mapping[wind_direction]]], dtype=np.float32)

        st.write("Running model prediction...")
        outputs = session.run(None, inputs)
        
        result = outputs[0][0][0]
        prediction = "Fire" if result > 0.5 else "No Fire"
        confidence = result if result > 0.5 else 1 - result

        st.subheader(f"🔥 Prediction Result: {prediction}")
        st.write(f"Confidence: {confidence:.2f}")

        # Store high-risk nodes for EWS transmission if fire is detected
        if prediction == "Fire":
            high_risk_node = {
                "name": "Node1",  # Replace with actual node identifier if available
                "lat": 18.8, "lon": 98.9,  # Replace with actual node coordinates if available
                "temperature": temperature,
                "humidity": humidity,
                "fire_risk": confidence,
            }
            if "high_risk_nodes" not in st.session_state:
                st.session_state.high_risk_nodes = []

            # Add to session state if not already added
            if not any(node["name"] == high_risk_node["name"] for node in st.session_state.high_risk_nodes):
                st.session_state.high_risk_nodes.append(high_risk_node)
                st.success(f"High-risk node '{high_risk_node['name']}' added to EWS transmission queue.")
            else:
                st.info(f"High-risk node '{high_risk_node['name']}' is already in the EWS queue.")

    # Add a note for users
    st.markdown("<div class='st-info'>Note: This demonstration uses a trained ONNX model for predictions.</div>", unsafe_allow_html=True)
