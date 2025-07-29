# routers/interview.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import schemas, auth, ai_analysis
from database import SessionLocal

router = APIRouter()

class InterviewRequest(BaseModel):
    question: str
    answer_text: str

class InterviewResponse(BaseModel):
    feedback: str
    next_question: str

@router.post("/analyze", response_model=InterviewResponse)
async def analyze_interview_answer(
    request: InterviewRequest,
    current_user: schemas.User = Depends(auth.get_current_user)
):
    if not request.answer_text.strip():
        raise HTTPException(status_code=400, detail="Answer text cannot be empty.")
    
    analysis_result = await ai_analysis.analyze_interview_conversation(
        question=request.question, 
        answer_text=request.answer_text
    )
    return analysis_result
