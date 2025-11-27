from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional, Tuple
from location_service import calculate_location_sens
from PIL.ExifTags import TAGS, GPSTAGS
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import io
import numpy as np
import time
import uuid

app = FastAPI(title="Chokho AI API")

# In-memory storage for complaints (will replace with PostgreSQL later)
complaints_db: List[Dict] = []

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

def get_location_from_exif(image : Image.Image) -> Tuple[Optional[float],Optional[float]]:
    try:
        exif_data = image.getexif()
        if not exif_data:
            print("No EXIF data found")
            return None, None
        
        gps_info = {}
        
        # Method 1: Try IFD (modern PIL) - GPS IFD tag is 34853
        if hasattr(exif_data, 'get_ifd'):
            gps_ifd = exif_data.get_ifd(34853)
            if gps_ifd:
                for tag_id, value in gps_ifd.items():
                    tag_name = GPSTAGS.get(tag_id, tag_id)
                    gps_info[tag_name] = value
        
        # Method 2: Fallback to old method if IFD didn't work
        if not gps_info:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'GPSInfo' and isinstance(value, dict):
                    for gps_tag, gps_value in value.items():
                        gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                        gps_info[gps_tag_name] = gps_value

        if not gps_info:
            print("No GPS info in EXIF")
            return None, None
        
        print(f"GPS info found: {list(gps_info.keys())}")
        
        def convert_to_degrees(value):
            if value is None:
                return None
            # Handle IFDRational or tuple
            if hasattr(value, '__iter__') and len(value) >= 3:
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
                return d + (m / 60.0) + (s / 3600.0)
            return None
        
        lat = convert_to_degrees(gps_info.get('GPSLatitude'))
        lng = convert_to_degrees(gps_info.get('GPSLongitude'))
        
        if lat is None or lng is None:
            print("Could not convert lat/lng")
            return None, None

        if gps_info.get('GPSLatitudeRef') == 'S':
            lat = -lat
        if gps_info.get('GPSLongitudeRef') == 'W':
            lng = -lng

        print(f"Extracted GPS: lat={lat}, lng={lng}")
        return lat, lng
    except Exception as e:
        print(f"GPS extraction failed : {e}")
        import traceback
        traceback.print_exc()
        return None, None

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
async def detect_trash(file : UploadFile = File(...)):
    try:
        contents = await file.read()
        
        # IMPORTANT: Extract EXIF BEFORE any image processing
        original_image = Image.open(io.BytesIO(contents))
        exif_lat, exif_lng = get_location_from_exif(original_image)
        
        # Now open again for detection (or reuse)
        image = Image.open(io.BytesIO(contents))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')

        if exif_lat and exif_lng :
            final_lat ,final_lng = exif_lat, exif_lng
            gps_source = "EXIF metadata"
        else:
            final_lat,final_lng = None,None
            gps_source = "Not available"

        if final_lat and final_lng:
            location_sens, reason, location_info = calculate_location_sens(final_lat,final_lng)
        else:
            location_sens = 5
            reason = "GPS not available - using default (residential)"
            location_info = None

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

        complaints_db.append({
            "id" : str(uuid.uuid4()),
            "latitude" : final_lat,
            "longitude" : final_lng,
            "severity_score" : severity,
            "urgency" : urgency,
            "color" : color,
            "timestamp" : datetime.now().isoformat(),
            "status" : "pending"
        })

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
            "location" : {
                "coordinates":{
                    "latitude" : final_lat,
                    "longitude" : final_lng
                } if final_lat else None,
                "gps_source" : gps_source,
                "sensitivity" : location_sens,
                "reason" : reason,
                "nearest_landmark" : location_info
            }
            ,
            "summary": {
                "total_objects": len(detections),
                "classes_detected": list(class_areas.keys()),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))

@app.get("/heatmap")
async def heatmap():
    return complaints_db