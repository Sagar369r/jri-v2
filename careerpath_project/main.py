# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import easyocr

# Import all the new router files
from routers import auth, users, assessment, interview
from database import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing OCR reader...")
    app.state.ocr_reader = easyocr.Reader(['en'])
    print("OCR reader initialized.")
    yield
    print("Closing application.")

app = FastAPI(
    title="JRI Career World API",
    description="A modular API service for JRI Career World.",
    lifespan=lifespan
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "null"
]
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
