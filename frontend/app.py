import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AI Medical Diagnosis", layout="wide", page_icon="🧠")

st.title("🧠 AI Medical Diagnosis Assistant")
st.markdown("Upload a Chest X-Ray to receive a Deep Learning-based prediction and an Explainable AI (Grad-CAM) heatmap.")

# Check API status
api_url = "http://localhost:8000"

try:
    response = requests.get(f"{api_url}/health")
    if response.status_code == 200:
        st.sidebar.success("✅ Backend API is Connected")
    else:
        st.sidebar.error("❌ Backend API Error")
except:
    st.sidebar.warning("⚠️ Could not connect to the Backend API. Ensure it is running.")

st.sidebar.header("Instructions")
st.sidebar.markdown(
    """
    1. Upload a valid Chest X-Ray image (JPG/PNG).
    2. The system will use a DenseNet121 model pre-trained on medical datasets to detect pathologies.
    3. A Grad-CAM heatmap will be generated to explain the prediction.
    """
)

uploaded_file = st.file_uploader("Choose a Chest X-Ray image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original X-Ray")
        img = Image.open(uploaded_file)
        st.image(img, use_column_width=True)

    with st.spinner("Analyzing image... This may take a moment."):
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Send to API
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        try:
            res = requests.post(f"{api_url}/predict", files=files)
            
            if res.status_code == 200:
                data = res.json()
                
                with col2:
                    st.subheader("Grad-CAM Heatmap")
                    heatmap_bytes = base64.b64decode(data["heatmap_base64"])
                    heatmap_img = Image.open(BytesIO(heatmap_bytes))
                    st.image(heatmap_img, use_column_width=True, caption="Red areas indicate regions of high importance for the prediction.")
                
                st.divider()
                
                # Display Results
                st.subheader("📊 Diagnostic Predictions")
                
                for pred in data["predictions"]:
                    pathology = pred["pathology"]
                    conf = pred["confidence"]
                    
                    st.markdown(f"**{pathology}**")
                    st.progress(conf / 100.0)
                    st.write(f"Confidence: {conf:.2f}%")
                
                st.divider()
                
                st.subheader("📝 Doctor-Friendly Report")
                st.info(data["report"])
                
            else:
                st.error(f"Error from API: {res.text}")
                
        except Exception as e:
            st.error(f"Failed to process image. Error: {e}")
