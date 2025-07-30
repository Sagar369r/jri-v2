# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Request
from sqlalchemy.orm import Session
import io, re
import crud, models, schemas, auth, ai_analysis, cloudinary_service
from database import SessionLocal

# New imports for pytesseract and image handling
import pytesseract
from PIL import Image

# Imports for handling PDF and DOCX files
import PyPDF2
import docx

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    email = auth.verify_access_token(token, credentials_exception)
    if email is None: raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None: raise credentials_exception
    return user

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.post("/me/resume", response_model=schemas.User)
async def upload_and_analyze_resume(
    request: Request,
    current_user: schemas.User = Depends(get_current_user),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    filename = file.filename.lower()
    text = ""
    
    if filename.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not read PDF file: {e}")
    elif filename.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(contents))
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not read DOCX file: {e}")
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        try:
            # --- UPDATED OCR LOGIC ---
            # Use Pillow to open the image from the uploaded file's bytes
            image = Image.open(io.BytesIO(contents))
            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(image)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not read image file with OCR: {e}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    analysis_results = await ai_analysis.analyze_resume_text(text)
    sanitized_text = text.replace('\x00', '')
    sanitized_analysis = analysis_results.replace('\x00', '')
    
    file_url = None
    try:
        file_url = cloudinary_service.upload_file_to_cloudinary(contents, file.filename, file.content_type)
        if file_url: print(f"Successfully uploaded to Cloudinary.")
        else: print("Cloudinary upload failed.")
    except Exception as e:
        print(f"Cloudinary upload error: {e}")

    return crud.update_user_resume_data(db, user_id=current_user.id, text=sanitized_text, analysis=sanitized_analysis, url=file_url)
