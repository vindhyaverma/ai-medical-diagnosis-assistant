FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required by OpenCV and other ML libraries
# Note: Using libgl1 instead of libgl1-mesa-glx for newer Debian (trixie) compatibility
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose ports for Hugging Face Spaces (7860 is strictly required)
EXPOSE 7860
EXPOSE 8000

# Command to run both using a simple shell script
# Streamlit MUST run on 7860 for Hugging Face Spaces to detect it
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false"]
