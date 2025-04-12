from ultralytics import YOLO
from sqlalchemy.orm import Session
from fastapi import HTTPException
from PIL import Image
import io, time, logging, json, torch
import numpy as np
from datetime import datetime
from ..models.waste_models import WasteType, RecyclingInstructions, DecompositionInfo
from ..config.db_config import settings

logging.basicConfig(level=logging.INFO)

try:
    with open("data/weights.json", "r") as f:
        weights_data = json.load(f)
        logging.info("Weights data loaded successfully.")
except Exception as e:
    logging.error(f"Error loading weights.json: {e}")
    weights_data = {}

def get_estimated_weight(waste_name: str) -> float:
    weight_str = weights_data.get(waste_name, "Unknown")
    if weight_str.lower() == "unknown":
        logging.warning(f"Weight not found for: {waste_name}")
        return 0.0
    try:
        return float(weight_str.replace(" grams", "").strip())
    except ValueError:
        logging.warning(f"Invalid weight format for: {waste_name}")
        return 0.0

def load_yolo_model():
    try:
        model = YOLO(settings.MODEL_PATH)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        logging.info(f"YOLO model loaded on {device}.")
        return model
    except Exception as e:
        logging.error(f"Error loading YOLO model: {e}")
        raise RuntimeError("Failed to load YOLO model.")

# Load the YOLO model at startup
model = load_yolo_model()

def classify_waste(image_bytes: bytes, db: Session):
    try:
        start_time = time.time()

        # Validate and process image
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img = img.resize((512, 512))  # Reduced size for better detection
            img_array = np.array(img)
        except Exception as e:
            logging.error(f"Invalid image format: {e}")
            raise HTTPException(status_code=400, detail="Invalid image format.")

        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            results = model.predict(img_array, device=device, conf=0.5)  # Reduced confidence threshold

            detected_items_dict = {}

            if not results or not hasattr(results[0], "boxes"):
                raise HTTPException(status_code=500, detail="YOLO model did not return valid detections.")

            for box in results[0].boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                detected_name = results[0].names.get(class_id, "Unknown").replace("-", " ").replace("_", " ")
                
                logging.info(f"Detected: {detected_name} (Confidence: {confidence})")
                
                if detected_name in detected_items_dict:
                    if detected_items_dict[detected_name]["confidence"] < confidence:
                        detected_items_dict[detected_name]["confidence"] = confidence
                else:
                    detected_items_dict[detected_name] = {"confidence": confidence}

            detected_items = []
            for detected_name, data in detected_items_dict.items():
                confidence = data["confidence"]

                waste_type = db.query(WasteType).filter(WasteType.name.ilike(f"%{detected_name}%")).first()
                
                if not waste_type:
                    logging.warning(f"No database match found for: {detected_name}")

                recycling_instruction = None
                decomposition_info = None

                if waste_type:
                    recycling_instruction = db.query(RecyclingInstructions).filter_by(waste_type_id=waste_type.id).first()
                    decomposition_info = db.query(DecompositionInfo).filter_by(waste_type_id=waste_type.id).first()
                    estimated_weight = get_estimated_weight(waste_type.name)
                    category = waste_type.category
                else:
                    estimated_weight = get_estimated_weight(detected_name)
                    category = "Unknown"

                detected_item = {
                    "waste_name": waste_type.name if waste_type else detected_name,
                    "category": category,
                    "confidence": confidence,
                    "estimated_weight": estimated_weight,
                    "recycling_instructions": recycling_instruction.instructions if recycling_instruction else "Not Available",
                    "decomposition_methods": {
                        "landfill": decomposition_info.landfill_decomposition if decomposition_info else "Not Available",
                        "ocean": decomposition_info.ocean_decomposition if decomposition_info else "Not Available",
                        "buried": decomposition_info.buried_decomposition if decomposition_info else "Not Available",
                        "open_environment": decomposition_info.open_environment_decomposition if decomposition_info else "Not Available"
                    }
                }

                detected_items.append(detected_item)

            execution_time = time.time() - start_time
            logging.info(f"Total classify_waste execution time: {execution_time:.2f} seconds")

            return detected_items 

        except Exception as e:
            logging.error(f"Error during classification: {e}")
            raise HTTPException(status_code=500, detail="Classification failed.")

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in classify_waste: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")