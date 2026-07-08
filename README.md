---
title: AI Medical Diagnosis Assistant
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🩺 Comprehensive AI Medical Assistant

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-FastAPI%20%7C%20Streamlit-green.svg" alt="Framework">
  <img src="https://img.shields.io/badge/AI-Gemini%201.5%20Pro%20%7C%20Llama%203.3-orange.svg" alt="AI Models">
  <img src="https://img.shields.io/badge/Deployment-Hugging%20Face-yellow.svg" alt="Deployment">
</div>

<br>

## 📖 Overview

The **Comprehensive AI Medical Assistant** is a cutting-edge multimodal AI application designed to act as an intelligent medical co-pilot for healthcare professionals and students. 

By leveraging state-of-the-art Vision-Language Models (VLMs) and Large Language Models (LLMs), this platform analyzes diverse medical data—including radiology imagery (X-Rays, MRIs) and text documents (PDF lab reports, patient history)—to provide instantaneous diagnostic summaries, clinical correlations, and evidence-based treatment guidance.

## ✨ Core Features

- **🧠 Multimodal Intelligence**: Upload multiple data modalities simultaneously. The AI can "look" at an X-Ray while simultaneously "reading" a blood test report to synthesize a holistic patient overview.
- **⚡ Dual AI Engines**: 
  - **Google Gemini 1.5 Pro**: Powered by LangChain, this engine handles complex Multimodal (Vision + Text) tasks.
  - **Groq (Llama 3.3 70B)**: Powered by Groq's custom LPU architecture, this engine provides lightning-fast analysis for purely text-based medical reports.
- **🏥 Doctor-Friendly Reporting**: Generates structured clinical notes including Patient Summaries, Laboratory Findings, Diagnoses, and Management Plans.
- **🔐 Bring Your Own Key (BYOK)**: Secure, stateless architecture where users supply their own API keys via the UI. Keys are never saved to the server.

## 🏗️ Architecture

This project is built using a modern microservice architecture deployed as a single unified Docker container:

1. **Frontend (Streamlit)**: A highly interactive, responsive web dashboard that handles file uploads, user prompts, API key management, and markdown rendering.
2. **Backend (FastAPI)**: A robust REST API that processes incoming files, utilizes `PyMuPDF` to extract text from documents, encodes images to base64, and orchestrates calls to the AI models via `LangChain`.
3. **Deployment (Docker)**: Both the frontend and backend are containerized into a single lightweight Debian Linux (`python:3.9-slim`) environment, ensuring cross-platform consistency and seamless deployment to Hugging Face Spaces.

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9+
- Docker (optional)

### Method 1: Running with Docker (Recommended)
```bash
# 1. Build the Docker Image
docker build -t medical-ai-assistant .

# 2. Run the Container
docker run -p 7860:7860 -p 8000:8000 medical-ai-assistant
```
*Note: Streamlit will be available at `http://localhost:7860` and FastAPI at `http://localhost:8000`.*

### Method 2: Running directly with Python
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the FastAPI Backend (Terminal 1)
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 3. Start the Streamlit Frontend (Terminal 2)
streamlit run frontend/app.py --server.port 7860
```

## 💡 Example Use Case

**Input:**
- *File 1*: A PDF detailing a 45-year-old patient presenting with fever, cough, and elevated WBC/CRP levels.
- *File 2*: A Chest X-Ray showing lower lobe consolidation.
- *Query*: "Analyze the attached chest X-ray and laboratory findings. Provide the most likely diagnosis."

**AI Output:**
The model successfully correlates the elevated inflammatory markers in the text with the visual consolidation in the X-Ray, accurately diagnosing **Community-Acquired Pneumonia (CAP)** and suggesting empiric antibiotic therapy and supportive care.

## ⚠️ Disclaimer
*This application is a portfolio project intended for educational and demonstrative purposes only. It is not a certified medical device. The AI-generated outputs should never be used as a substitute for professional medical advice, diagnosis, or treatment.*
