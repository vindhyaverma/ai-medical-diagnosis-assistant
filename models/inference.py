import os
import torch
import torchvision
import torchxrayvision as xrv
from PIL import Image
import numpy as np
import cv2
import base64
from io import BytesIO
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from skimage.color import rgba2rgb, gray2rgb

# Load the pre-trained DenseNet model from torchxrayvision
# The "densenet121-res224-all" weights are trained on a combination of massive datasets (NIH, CheXpert, etc.)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Loading Model on {device}...")
model = xrv.models.DenseNet(weights="densenet121-res224-all").to(device)
model.eval()

# Get the pathologies the model was trained to predict
pathologies = model.pathologies

# Define the transform required by torchxrayvision
transform = torchvision.transforms.Compose([
    xrv.datasets.XRayCenterCrop(),
    xrv.datasets.XRayResizer(224)
])

def process_image(image_bytes: bytes):
    """
    Reads image bytes and prepares them for torchxrayvision.
    """
    img = Image.open(BytesIO(image_bytes)).convert("L") # Convert to grayscale
    img_np = np.array(img)
    
    # Normalize image to [-1024, 1024] as required by torchxrayvision
    img_np = xrv.datasets.normalize(img_np, 255) 
    
    # Add color channel
    img_np = img_np[None, ...]
    
    # Apply transforms
    img_tensor = transform(img_np)
    img_tensor = torch.from_numpy(img_tensor).unsqueeze(0).to(device)
    return img_tensor, img

def generate_report(top_predictions):
    """
    Generates a template-based doctor-friendly NLP report based on the top predictions.
    """
    if not top_predictions:
        return "No significant pathologies detected with high confidence."
        
    report = f"The model has analyzed the chest X-Ray and predicts {top_predictions[0]['pathology']} with a confidence of {top_predictions[0]['confidence']:.1f}%. "
    
    if len(top_predictions) > 1:
        report += f"Additionally, there are secondary indicators of {top_predictions[1]['pathology']} ({top_predictions[1]['confidence']:.1f}%). "
        
    report += "\n\nThe Grad-CAM heatmap highlights the specific regions of the lung field that contributed most significantly to the primary prediction. "
    report += "Please correlate clinically."
    
    return report

def predict(image_bytes: bytes):
    """
    Runs inference and generates a Grad-CAM heatmap.
    """
    img_tensor, original_img = process_image(image_bytes)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        
    preds = outputs[0].cpu().numpy()
    
    # Create a list of dictionaries with pathology and confidence
    results = []
    for i, p in enumerate(pathologies):
        # outputs are technically unnormalized logits or probabilities depending on the version,
        # but torchxrayvision models output probabilities between 0 and 1.
        confidence = float(preds[i]) * 100
        results.append({
            "pathology": p,
            "confidence": confidence
        })
        
    # Sort by highest confidence
    results.sort(key=lambda x: x["confidence"], reverse=True)
    top_3 = results[:3]
    
    # --- Grad-CAM ---
    # Target the last convolutional block of the DenseNet
    target_layers = [model.features[-1]]
    
    # We want to explain the highest confidence prediction
    target_idx = pathologies.index(top_3[0]["pathology"])
    targets = [ClassifierOutputTarget(target_idx)]
    
    # Initialize CAM
    cam = GradCAM(model=model, target_layers=target_layers) # Removed use_cuda as it's deprecated in newer versions. It infers from model device.
    
    # Generate heatmap
    grayscale_cam = cam(input_tensor=img_tensor, targets=targets)[0, :]
    
    # Overlay on original image
    # Need to resize original image to 224x224 and convert to RGB (0-1 float)
    orig_resized = original_img.resize((224, 224))
    orig_rgb = gray2rgb(np.array(orig_resized)) / 255.0
    
    visualization = show_cam_on_image(orig_rgb, grayscale_cam, use_rgb=True)
    
    # Convert heatmap back to PIL image and then to base64
    vis_img = Image.fromarray(visualization)
    buffered = BytesIO()
    vis_img.save(buffered, format="JPEG")
    heatmap_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    report = generate_report(top_3)
    
    return {
        "predictions": top_3,
        "report": report,
        "heatmap": heatmap_b64
    }
