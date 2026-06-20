import cv2
import os
from ultralytics import YOLO

# 1. Load model ONCE globally (outside the function)
# This keeps the model in GPU memory for fast inference on every frame
model = YOLO('yolo11n.pt') 

def process_cricket_video(video_path: str, output_path: str):
    print(f"Starting detection on {video_path}...")

    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 2. Use stream=True and tracker if needed
        # Using device='0' for GPU acceleration
        results = model.predict(frame, device='0', conf=0.25, stream=True)
        
        # Visualize
        for result in results:
            annotated_frame = result.plot()
            out.write(annotated_frame)
        
    cap.release()
    out.release()
    print(f"Processing complete! Saved to {output_path}")