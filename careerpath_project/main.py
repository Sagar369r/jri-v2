# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
# easyocr is no longer needed
import os 

# Import all the new router files
from routers import auth, users, assessment, interview
from database import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # The easyocr reader is no longer initialized at startup
    print("Lifespan start: Application is ready.")
    yield
    print("Closing application.")

app = FastAPI(
    title="JRI Career World API",
    description="A modular API service for JRI Career World.",
    lifespan=lifespan
)

# --- Deployment-Ready CORS Configuration ---
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://jri-v2.vercel.app"
    "null"
]

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include all the routers from the other files ---
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(assessment.router, prefix="/assessment", tags=["Assessment"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to JRI Career World API"}
