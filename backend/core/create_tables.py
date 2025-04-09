from config.db_config import engine
from models.base import Base
from models.feedback_models import UserFeedback
from models.user_models import User
from models.waste_models import WasteType, RecyclingInstructions, DecompositionInfo, WasteRecord

print("Creating tables...")
Base.metadata.create_all(engine)  
print("Tables created successfully!")
