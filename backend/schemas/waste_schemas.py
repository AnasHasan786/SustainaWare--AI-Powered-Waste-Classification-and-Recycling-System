from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import relationship

# ----------------- WasteType Schema ---------------------
class WasteTypeBase(BaseModel):
    """Base schema for waste types"""
    name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=100) 

class WasteTypeCreate(WasteTypeBase):
    """Schema for creating a new waste type"""
    pass


class WasteType(WasteTypeBase):
    """Schema for retrieving waste type data"""
    id: str
    recycling_instructions: Optional[list["RecyclingInstructions"]] = None

    @classmethod
    def from_orm(cls, obj):
        """Custom method to handle UUID conversion"""
        obj.id = str(obj.id)  
        return super().from_orm(obj)
    
    class Config:
        from_attributes = True
        json_encoders = {UUID: str}

class WasteCategoryStats(BaseModel):
    category: str
    count: int

class WasteStatsResponse(BaseModel):
    data: List[WasteCategoryStats]

# ----------------- RecyclingInstructions Schema ---------------------
class Instruction(BaseModel):
    """Schema for an individual recycling instruction step"""
    step: int
    title: str
    description: str

class RecyclingInstructionsBase(BaseModel):
    """Base schema for recycling instructions"""
    instructions: list[Instruction] = Field(..., min_items=1)

class RecyclingInstructionsCreate(RecyclingInstructionsBase):
    """Schema for creating recycling instructions"""
    waste_type_id: str

class RecyclingInstructions(RecyclingInstructionsBase):
    """Schema for retrieving recycling instructions"""
    id: str
    waste_type_id: str

    class Config:
        model_config = {"from_attributes": True}


# ----------------- DecompositionInfo Schema ---------------------
from typing import Optional, Dict
from pydantic import BaseModel, Field

class DecompositionInfoBase(BaseModel):
    """Base schema for decomposition information"""
    landfill_decomposition: Optional[Dict] = None
    ocean_decomposition: Optional[Dict] = None
    buried_decomposition: Optional[Dict] = None
    open_environment_decomposition: Optional[Dict] = None
    recycling_process: Optional[Dict] = None

class DecompositionInfoCreate(DecompositionInfoBase):
    """Schema for creating decomposition information"""
    waste_type_id: str


class DecompositionInfo(DecompositionInfoBase):
    """Schema for retrieving decomposition information"""
    id: str
    waste_type_id: str

    class Config:
        orm_mode = True  
        

# ----------------- DisposalMethod Schema ---------------------
class DisposalMethodBase(BaseModel):
    """Base schema for disposal methods"""
    best_method: str = Field(..., min_length=5, max_length=500)


class DisposalMethodCreate(DisposalMethodBase):
    """Schema for creating disposal methods"""
    waste_type_id: str


class DisposalMethod(DisposalMethodBase):
    """Schema for retrieving disposal methods"""
    id: str
    waste_type_id: str

    class Config:
        model_config = {"from_attributes": True}


# ----------------- WasteRecord Schema ---------------------
class WasteRecordBase(BaseModel):
    """Base schema for waste records"""
    waste_name: str = Field(..., min_length=2, max_length=100)
    waste_category: str = Field(..., min_length=2, max_length=100)
    estimated_weight: Optional[float] = Field(None, ge=0)
    recycling_instructions: Optional[str] = Field(None, max_length=1000)
    soil_decomposition: Optional[str] = Field(None, max_length=500)
    water_decomposition: Optional[str] = Field(None, max_length=500)
    landfill_decomposition: Optional[str] = Field(None, max_length=500)
    best_disposal_method: Optional[str] = Field(None, max_length=500)


class WasteRecordCreate(WasteRecordBase):
    """Schema for creating waste records"""
    pass


class WasteRecord(WasteRecordBase):
    """Schema for retrieving waste records"""
    id: str

    class Config:
        model_config = {"from_attributes": True}
