from fastapi import FastAPI, File, UploadFile, Form
from typing import List, Optional
import fitz  # PyMuPDF
import base64
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os

app = FastAPI(title="Multimodal Medical AI Backend")

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_medical_data(
    provider: str = Form(...),
    api_key: str = Form(...),
    query: str = Form(...),
    files: List[UploadFile] = File(default=[])
):
    try:
        content_parts = [{"type": "text", "text": query}]
        
        has_image = False
        
        for file in files:
            file_bytes = await file.read()
            
            if file.filename.lower().endswith(".pdf"):
                # Extract text from PDF
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                pdf_text = ""
                for page in doc:
                    pdf_text += page.get_text()
                content_parts.append({"type": "text", "text": f"\n\n--- Document: {file.filename} ---\n{pdf_text}\n--- End Document ---\n"})
                
            elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                has_image = True
                # Add image
                img_b64 = base64.b64encode(file_bytes).decode("utf-8")
                content_parts.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                })
                
        # Initialize the model based on provider
        if provider == "Groq":
            if has_image:
                return {"error": "Groq currently only supports text-based files (like PDFs). Please remove the image/X-Ray or switch to Gemini to analyze images."}
            
            os.environ["GROQ_API_KEY"] = api_key
            llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
        else:
            os.environ["GOOGLE_API_KEY"] = api_key
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
            
        message = HumanMessage(content=content_parts)
        response = llm.invoke([message])
        
        return {"response": response.content}
        
    except Exception as e:
        return {"error": str(e)}
