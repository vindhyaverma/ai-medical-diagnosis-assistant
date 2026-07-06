---
title: AI Medical Diagnosis Assistant
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🧠 AI Medical Diagnosis Assistant

## Overview
An end-to-end platform that ingests medical images (X-rays, MRIs) and uses Deep Learning (CNNs, Vision Transformers) to predict diseases with an explainable AI (XAI) heatmap (Grad-CAM).

I built this project to demonstrate a complete, production-ready AI pipeline. It moves beyond a simple Jupyter Notebook by integrating a robust backend API and an interactive frontend dashboard, all containerized for easy deployment.

## Tech Stack
- **Tools & Frameworks**: Python, PyTorch, CNN/ViT, Grad-CAM, Streamlit, FastAPI, Docker

## Key Features
- Upload X-ray/MRI
- Disease prediction
- Confidence score
- Heatmap explanation
- Doctor-friendly report

## Architecture
1. **Frontend (Streamlit)**: Provides an interactive dashboard for users to upload data, view results, and interact with the AI models.
2. **Backend (FastAPI)**: A high-performance, asynchronous API that handles incoming requests, orchestrates the AI model inference, and returns results.
3. **AI Models**: The core machine learning logic (pre-trained/MVP models used for rapid deployment demonstration).
4. **Deployment (Docker)**: The entire application is containerized using Docker and Docker Compose, ensuring environment consistency and easy cloud deployment.

## How to Run (Local Deployment)

### Prerequisites
- Docker & Docker Compose installed on your machine.

### Steps
1. Clone this repository.
2. Navigate to the project directory:
   ```bash
   cd ai-medical-diagnosis-assistant
   ```
3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
4. Access the applications:
   - **Frontend Dashboard**: `http://localhost:8501`
   - **Backend API (Swagger Docs)**: `http://localhost:8000/docs`

## Developer Notes
*This project was developed with a focus on clean architecture, API-first design, and MLOps best practices (containerization).*
