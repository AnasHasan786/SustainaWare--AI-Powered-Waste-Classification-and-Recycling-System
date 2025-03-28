from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers
from .routers.auth import router as auth_router
from .routers.users import router as users_router
from .routers.waste import router as waste_router
from .routers.feedback import router as feedback_router
from .routers.waste_classification import router as classification_router
from .routers.nlp import router as nlp_router 

# Initialize FastAPI app
app = FastAPI(title="SustainaWare API", version="1.0.0")

# Configure CORS middleware
origins = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", tags=["General"])
async def read_root():
    return {"message": "SustainaWare API is running!"}

# Health check endpoint
@app.get("/health", tags=["General"])
async def health_check():
    try:
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

# Register Routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(waste_router, prefix="/api/waste", tags=["Waste Management"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(classification_router, prefix="/api/waste/classify", tags=["Classification"])
app.include_router(nlp_router, prefix="/api/nlp", tags=["NLP"]) 
