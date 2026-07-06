from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# We will import the ML logic we just created
from models.inference import predict

app = FastAPI(
    title="AI Medical Diagnosis API",
    description="Backend API for processing Chest X-Rays, predicting diseases, and generating XAI heatmaps."
)

# Enable CORS for the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Medical AI API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
async def process_xray(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    try:
        contents = await file.read()
        
        # Call the inference logic
        result = predict(contents)
        
        return {
            "status": "success",
            "predictions": result["predictions"],
            "report": result["report"],
            "heatmap_base64": result["heatmap"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
