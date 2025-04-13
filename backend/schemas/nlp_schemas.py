from pydantic import BaseModel, conint
from typing import Optional

class NLPRequest(BaseModel):
    """
    Schema for incoming NLP requests.
    """
    text: str
    max_length: Optional[conint(ge=1)] = 100  # type: ignore

    class Config:
        json_schema_extra = {
            "example": {
                "text": "How do I recycle plastic bottles responsibly?",
                "max_length": 100
            }
        }

class NLPResponse(BaseModel):
    """
    Schema for NLP responses.
    """
    response: str
    status: str = "success"
    details: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Plastic bottles can be recycled by rinsing and placing them in designated recycling bins.",
                "status": "success",
                "details": "Recycling tips provided based on query."
            }
        }

class NLPErrorResponse(BaseModel):
    """
    Schema for error responses in NLP operations.
    """
    error: str
    status: str = "error"
    details: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Failed to process the input text.",
                "status": "error",
                "details": "Model inference failed due to invalid input."
            }
        }
