import uuid 
from sqlalchemy import Column, String, Index, DateTime, func, ForeignKey, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


# ---------------------- WasteType Model ----------------------
class WasteType(Base):
    __tablename__ = 'waste_types'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    recycling_instructions = relationship("RecyclingInstructions", back_populates="waste_type", uselist=False)
    decomposition_info = relationship("DecompositionInfo", back_populates="waste_type", uselist=False)
    waste_records = relationship("WasteRecord", back_populates="waste_type")

    __table_args__ = (
        Index('ix_waste_name', 'name'),
    )

    def __repr__(self):
        return f"<WasteType(id={str(self.id)}, name={self.name}, category={self.category}, created_at={self.created_at})>"

    class Config:
        orm_mode = True


# ------------------- RecyclingInstructions Model -------------------
class RecyclingInstructions(Base):
    __tablename__ = 'recycling_instructions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waste_type_id = Column(UUID(as_uuid=True), ForeignKey('waste_types.id'), nullable=False, unique=True)
    instructions = Column(JSON, nullable=False)

    waste_type = relationship("WasteType", back_populates="recycling_instructions")

    def __repr__(self):
        return f"<RecyclingInstructions(id={str(self.id)}, waste_type_id={str(self.waste_type_id)}, instructions={self.instructions})>"

    class Config:
        orm_mode = True


# -------------------- DecompositionInfo Model --------------------
class DecompositionInfo(Base):
    __tablename__ = 'decomposition_info'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waste_type_id = Column(UUID(as_uuid=True), ForeignKey('waste_types.id'), nullable=False, unique=True)
    
    landfill_decomposition = Column(JSON, nullable=True)
    ocean_decomposition = Column(JSON, nullable=True)
    buried_decomposition = Column(JSON, nullable=True)
    open_environment_decomposition = Column(JSON, nullable=True)
    recycling_process = Column(JSON, nullable=True)

    waste_type = relationship("WasteType", back_populates="decomposition_info")

    def __repr__(self):
        return (
            f"<DecompositionInfo(id={str(self.id)}, waste_type_id={str(self.waste_type_id)}, "
            f"landfill_decomposition={self.landfill_decomposition}, ocean_decomposition={self.ocean_decomposition}, "
            f"buried_decomposition={self.buried_decomposition}, open_environment_decomposition={self.open_environment_decomposition}, "
            f"recycling_process={self.recycling_process}, impact_on_environment={self.impact_on_environment}, "
            f"recyclability={self.recyclability}, decomposition_factors={self.decomposition_factors})>"
        )

    class Config:
        orm_mode = True


# ---------------------- WasteRecord Model ----------------------
class WasteRecord(Base):
    __tablename__ = 'waste_records'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waste_name = Column(String(255), nullable=False)
    waste_category = Column(String(50), nullable=False)
    estimated_weight = Column(Float, nullable=True)
    recycling_instructions = Column(String(1000), nullable=True)
    soil_decomposition = Column(String(500), nullable=True)
    water_decomposition = Column(String(500), nullable=True)
    landfill_decomposition = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    waste_type_id = Column(UUID(as_uuid=True), ForeignKey('waste_types.id'), nullable=True)

    waste_type = relationship("WasteType", back_populates="waste_records")

    def __repr__(self):
        return f"<WasteRecord(id={str(self.id)}, waste_name={self.waste_name}, waste_category={self.waste_category}, estimated_weight={self.estimated_weight})>"

    class Config:
        orm_mode = True
