from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from ultralytics import YOLO
from PIL import Image
import io
import numpy as np
import time

app = FastAPI(title="Chokho AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

MODEL_PATH = "../chokho_ai.pt"
model = YOLO(MODEL_PATH)

CONFIDENCE_THRESHOLDS = {
    'plastic' : 0.25,
    'metal' : 0.45,
    'paper' : 0.40,
    'glass' : 0.55,
    'organic' : 0.35,
    'bin' : 0.65
}

SEVERITY_WEIGHTS = {
    'plastic' : 6,
    'metal' : 5,
    'paper' : 3,
    'glass' : 5,
    'organic' : 3,
    'bin' : 4
}

def filter_and_analyze_detections(results, thresholds: Dict[str,float] , image_width : int , image_height : int):
    detections = []
    total_area = 0
    class_areas = {}

    image_total_area = image_width * image_height

    for result in results:
        boxes = result.boxes

        for box in boxes:
            cls_idx = int(box.cls[0])
            cls_name = model.names[cls_idx]
            confidence = float(box.conf[0])

            threshold = thresholds.get(cls_name,0.5)

            if confidence >= threshold:
                bbox = box.xyxy[0].tolist()

                area_pixels = calculate_bbox_area(bbox)
                area_percentage = (area_pixels/image_total_area) * 100

                if cls_name not in class_areas:
                    class_areas[cls_name] = 0
                class_areas[cls_name] += area_pixels

                total_area += area_pixels

                detections.append({
                    'class': cls_name,
                    'confidence' : round(confidence,3),
                    'threshold_used' : threshold,
                    'bbox' : {
                        'x1' : round(bbox[0],2),
                        'y1' : round(bbox[1],2),
                        'x2' : round(bbox[2],2),
                        'y2' : round(bbox[3], 2)
                    },
                    'area':{
                        'pixels' : round(area_pixels,2),
                        'percentage' : round(area_percentage,2)
                    }
                })
            
    return detections, total_area, class_areas, image_total_area

def calculate_severity(detections: List[dict], total_area : float, class_areas : Dict[str,float], image_total_area : float , location_sens: int=5):
    if not detections:
        return 0, {}
    
    type_score = 0

    for cls_name, area in class_areas.items():
        weight = SEVERITY_WEIGHTS.get(cls_name,5)
        area_ratio = area/total_area
        type_score += weight * area_ratio

    type_score = min(type_score,10)

    location_score = location_sens

    area_coverage = (total_area/image_total_area) *100

    if area_coverage >= 50:
        area_score = 10
    elif area_coverage >= 30:
        area_score = 8
    elif area_coverage >= 15:
        area_score = 6
    elif area_coverage >= 5:
        area_score = 4
    else:
        area_score = 2

    severity = (type_score*0.5) + (location_score*0.3) + (area_score*0.2)

    breakdown = {
        'type_score' : round(type_score,2),
        'location_score' : location_score,
        'area_score' : area_score,
        'area_coverage_percent' : round(area_coverage,2)
    }

    return round(severity,1), breakdown


def calculate_bbox_area(bbox: List[float]) -> float:
    x1,y1,x2,y2 = bbox
    width = x2 - x1
    height = y2 - y1
    return width * height


@app.get("/")
def root():
    return{
        "message" : "Chokho AI API",
        "model" : "YOLOv11n",
        "version" : "1.0",
    }

@app.post("/detect")
async def detect_trash(file : UploadFile = File(...), location_sens: int = 5):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        img_width , img_height = image.size

        start_time = time.time()
        results = model(image, verbose = False)
        inference_time = time.time() - start_time

        detections, total_area , class_areas , image_area = filter_and_analyze_detections(results, CONFIDENCE_THRESHOLDS, img_width, img_height)

        if len(detections) < 1:
            return{
                "success" : False
            }

        severity, breakdown = calculate_severity(detections,total_area,class_areas,image_area, location_sens)

        if severity >= 8:
            urgency = "URGENT"
            eta_hours = 13
            color = "red"
        elif severity >= 5:
            urgency = "MEDIUM"
            eta_hours = 24
            color = "orange"
        else:
            urgency = "LOW"
            eta_hours = 48
            color = "yellow"

        return{
            "success" : True,
            "detections" : detections,
            "severity": {
                "score": severity,
                "urgency": urgency,
                "color": color,
                "estimated_eta_hours": eta_hours,
                "breakdown": breakdown
            },
            "summary": {
                "total_objects": len(detections),
                "classes_detected": list(class_areas.keys()),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))