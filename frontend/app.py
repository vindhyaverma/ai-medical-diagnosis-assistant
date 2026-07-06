import streamlit as st
import requests

st.set_page_config(page_title="AI Medical Assistant", layout="wide", page_icon="🩺")

st.title("🩺 Comprehensive AI Medical Assistant")
st.markdown("Upload medical reports (PDFs) and images (X-Rays, MRIs) to get instant, AI-driven medical insights, diagnoses, and guidance.")

api_url = "http://localhost:8000"

with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("[Get your API Key here](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    
    # API Health Check
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Error")
    except:
        st.warning("⚠️ Could not connect to Backend")

# File Uploader
uploaded_files = st.file_uploader("Upload Medical Files (PDFs or Images)", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

query = st.text_area("What would you like to know about these files?", value="Please analyze these medical documents and provide a comprehensive diagnostic summary, potential next steps, and any prescription or treatment guidance based on the findings.")

if st.button("Analyze with AI Doctor", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not uploaded_files and not query:
        st.warning("Please upload files or enter a query.")
    else:
        with st.spinner("Analyzing your medical data..."):
            
            # Prepare files for the request
            files_to_send = []
            for file in uploaded_files:
                files_to_send.append(("files", (file.name, file.getvalue(), file.type)))
            
            data = {
                "api_key": api_key,
                "query": query
            }
            
            try:
                if len(files_to_send) > 0:
                    res = requests.post(f"{api_url}/analyze", data=data, files=files_to_send)
                else:
                    res = requests.post(f"{api_url}/analyze", data=data)
                    
                if res.status_code == 200:
                    response_data = res.json()
                    if "error" in response_data:
                        st.error(f"Error from AI Model: {response_data['error']}")
                    else:
                        st.subheader("👨‍⚕️ AI Doctor's Report")
                        st.write(response_data["response"])
                else:
                    st.error(f"Backend error: {res.text}")
                    
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

