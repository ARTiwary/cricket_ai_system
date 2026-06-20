from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from detector import process_cricket_video
import os
import shutil

app = FastAPI(title="Cricket AI Backend")

# 1. CORS setup to allow your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Directory Setup
UPLOAD_DIR = "data/raw"
OUTPUT_DIR = "data/processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Create file paths
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    output_filename = f"processed_{file.filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Save the uploaded file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 3. Add the AI processing to BackgroundTasks
    # This keeps the API responsive while the GPU works
    background_tasks.add_task(process_cricket_video, file_path, output_path)
    
    return {
        "message": "Analysis started successfully", 
        "file": file.filename,
        "output_expected": output_filename
    }

@app.get("/")
def health_check():
    return {"status": "Backend is active and ready for inference"}