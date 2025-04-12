from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from ..config.db_config import get_db
from ..services.auth_service import get_current_admin
from ..models.waste_models import WasteType, WasteRecord, RecyclingInstructions, DecompositionInfo
from ..schemas.waste_schemas import (
    WasteType as WasteTypeSchema,
    WasteTypeCreate,
    WasteRecordCreate,
    WasteRecord as WasteRecordSchema,
    RecyclingInstructionsCreate,
    DecompositionInfoCreate
)
import json

router = APIRouter(prefix="/waste", tags=["Waste Management"])

# ------------------ Waste Types ------------------
@router.get("/", response_model=list[WasteTypeSchema], status_code=status.HTTP_200_OK)
async def get_waste_types(db: Session = Depends(get_db)):
    """
    Retrieve all waste types.
    """
    waste_types = db.query(WasteType).all()
    if not waste_types:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No waste types found."
        )
    formatted_waste_types = [
        WasteTypeSchema(**{**waste.__dict__, "id": str(waste.id)})
        for waste in waste_types
    ]
    return formatted_waste_types

@router.post("/", response_model=WasteTypeSchema, status_code=status.HTTP_201_CREATED)
async def create_waste_type(
    waste_type: WasteTypeCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """
    Create a new waste type. Restricted to admin users.
    """
    existing_waste = db.query(WasteType).filter(WasteType.name.ilike(waste_type.name)).first()
    if existing_waste:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Waste type '{waste_type.name}' already exists."
        )
    new_waste_type = WasteType(name=waste_type.name, category=waste_type.category)
    db.add(new_waste_type)
    db.commit()
    db.refresh(new_waste_type)
    return WasteTypeSchema(**{**new_waste_type.__dict__, "id": str(new_waste_type.id)})

# ------------------ Waste Records ------------------
@router.post("/records/", response_model=WasteRecordSchema, status_code=status.HTTP_201_CREATED)
async def create_waste_record(
    waste_record: WasteRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new waste classification record.
    """
    new_record = WasteRecord(**waste_record.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/records/", response_model=list[WasteRecordSchema], status_code=status.HTTP_200_OK)
async def get_waste_records(db: Session = Depends(get_db)):
    """
    Retrieve all waste classification records.
    """
    records = db.query(WasteRecord).all()
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No waste records found."
        )
    return records

# ------------------ Recycling Instructions ------------------
@router.post("/{waste_type_name}/recycling", status_code=status.HTTP_201_CREATED)
async def create_recycling_instructions(
    waste_type_name: str,
    instructions: RecyclingInstructionsCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """
    Create recycling instructions for a specific waste type.
    """
    waste = db.query(WasteType).filter(WasteType.name.ilike(waste_type_name)).first()
    if not waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Waste type '{waste_type_name}' not found."
        )
    if waste.recycling_instructions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Recycling instructions for '{waste_type_name}' already exist."
        )
    recycling_instruction = RecyclingInstructions(
        waste_type_id=waste.id,
        instructions=[instr.dict() for instr in instructions.instructions]
    )
    db.add(recycling_instruction)
    db.commit()
    db.refresh(recycling_instruction)
    return {"message": f"Recycling instructions for '{waste_type_name}' created successfully."}


@router.get("/{waste_type_name}/recycling", status_code=status.HTTP_200_OK)
async def get_recycling_instructions(waste_type_name: str, db: Session = Depends(get_db)):
    """
    Get recycling instructions for a specific waste type.
    """
    waste = (
        db.query(WasteType)
        .options(joinedload(WasteType.recycling_instructions))  # Eager load instructions
        .filter(WasteType.name.ilike(waste_type_name))
        .first()
    )
    if not waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recycling instructions for '{waste_type_name}' not found.",
        )
    return {"recycling_instructions": waste.recycling_instructions}


# ------------------ Decomposition Environments ------------------
@router.post("/{waste_type_name}/decomposition", status_code=status.HTTP_201_CREATED)
async def create_decomposition_info(
    waste_type_name: str,
    decomposition_data: DecompositionInfoCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """
    Create decomposition information for a specific waste type.
    """
    waste = db.query(WasteType).filter(WasteType.name.ilike(waste_type_name)).first()
    if not waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Waste type '{waste_type_name}' not found."
        )

    decomposition_info = DecompositionInfo(
        waste_type_id=waste.id,
        landfill_decomposition=decomposition_data.landfill_decomposition,  
        ocean_decomposition=decomposition_data.ocean_decomposition, 
        buried_decomposition=decomposition_data.buried_decomposition,  
        open_environment_decomposition=decomposition_data.open_environment_decomposition,  
        recycling_process=decomposition_data.recycling_process,  
    )

    db.add(decomposition_info)
    db.commit()
    db.refresh(decomposition_info)

    return {"message": f"Decomposition information for '{waste_type_name}' created successfully."}


@router.get("/{waste_type_name}/decomposition", status_code=status.HTTP_200_OK)
async def get_decomposition_info(waste_type_name: str, db: Session = Depends(get_db)):
    """
    Get decomposition information details for a specific waste type.
    """
    waste = db.query(WasteType).filter(WasteType.name.ilike(waste_type_name)).first()
    if not waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decomposition information for '{waste_type_name}' not found."
        )

    decomposition_info = db.query(DecompositionInfo).filter(DecompositionInfo.waste_type_id == waste.id).first()
    if not decomposition_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decomposition information for '{waste_type_name}' not found."
        )

    # Convert the decomposition info into a JSON-friendly format
    return {
        "decomposition_info": {
            "landfill_decomposition": decomposition_info.landfill_decomposition,
            "ocean_decomposition": decomposition_info.ocean_decomposition,
            "buried_decomposition": decomposition_info.buried_decomposition,
            "open_environment_decomposition": decomposition_info.open_environment_decomposition,
            "recycling_process": decomposition_info.recycling_process,
        }
    }

