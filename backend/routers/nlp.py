from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas.auth_schemas import User
from ..schemas.nlp_schemas import NLPRequest, NLPResponse
from ..services.nlp_service import NLPModel
from ..config.db_config import get_db
from ..services.auth_service import get_current_user

router = APIRouter(
    prefix="/nlp",
    tags=["NLP"],
    responses={404: {"description": "Not found"}},
)

# Initialize the NLP model instance
nlp_model = NLPModel()

@router.post("/predict", response_model=NLPResponse)
async def predict_text(
    request: NLPRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        response_text = nlp_model.get_response(request.text) 

        return NLPResponse(response=response_text)  

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

