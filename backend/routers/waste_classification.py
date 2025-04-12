from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from ..services import classification_service
from ..config.db_config import get_db
import time
import logging
import imghdr

router = APIRouter(prefix="/classify", tags=["Classification"])

@router.post("/", status_code=status.HTTP_200_OK)
async def classify_waste_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    start_time = time.time()
    try:
        # Validate file content type
        if not file.content_type.startswith("image/"):
            logging.error(f"Invalid content type: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Uploaded file is not an image. Content type: {file.content_type}"
            )

        # Read file bytes
        image_bytes = await file.read()

        # Validate image format using imghdr
        image_format = imghdr.what(None, image_bytes)
        if image_format not in ["jpeg", "png", "gif", "bmp", "tiff"]:
            logging.error(f"Unsupported image format: {image_format}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image format: {image_format}"
            )

        # Classify the waste
        waste_data = classification_service.classify_waste(image_bytes, db)

        # Measure execution time
        execution_time = time.time() - start_time
        logging.info(
            f"Classify waste execution time: {execution_time:.2f} seconds for file '{file.filename}'"
        )

        # Return the classification result
        return {
            "success": True,
            "message": "Waste classification successful",
            "execution_time": execution_time,
            "classification": waste_data
        }

    except HTTPException as e:
        logging.error(
            f"Error processing file '{file.filename}': {e.detail}"
        )
        raise e
    except Exception as e:
        logging.error(
            f"Unexpected error occurred while processing file '{file.filename}': {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the image."
        )
