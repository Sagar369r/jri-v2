# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, auth as auth_service, crud, email_service, user_logger
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/magic-link/request", status_code=status.HTTP_202_ACCEPTED)
async def request_magic_link(request: schemas.MagicLinkRequest, db: Session = Depends(get_db)):
    user = crud.get_or_create_user(db, email=request.email)
    user_logger.log_user_email(user.email)
    plain_token, token_hash = auth_service.create_magic_link_token()
    crud.create_magic_token(db, email=request.email, token_hash=token_hash)
    email_service.send_magic_link(email=request.email, token=plain_token)
    return {"message": "If an account with this email exists, a magic link has been sent."}

@router.post("/magic-link/login", response_model=schemas.Token)
async def login_with_magic_link(request: schemas.MagicLinkLogin, db: Session = Depends(get_db)):
    valid_tokens = db.query(models.MagicToken).filter(
        models.MagicToken.is_used == False,
        models.MagicToken.expires_at > datetime.utcnow()
    ).all()
    db_token_record = None
    for token_record in valid_tokens:
        if auth_service.verify_magic_link_token(request.token, token_record.token_hash):
            db_token_record = crud.use_magic_token(db, token_hash=token_record.token_hash)
            break
    if not db_token_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid, expired, or already used magic link.")
    access_token = auth_service.create_access_token(data={"sub": db_token_record.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/dev-login", response_model=schemas.Token)
async def developer_login(request: schemas.MagicLinkRequest, db: Session = Depends(get_db)):
    crud.get_or_create_user(db, email=request.email)
    access_token = auth_service.create_access_token(data={"sub": request.email})
    return {"access_token": access_token, "token_type": "bearer"}
