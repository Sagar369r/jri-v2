# routers/assessment.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import json, re
import crud, models, schemas, auth, ai_analysis, email_service
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/questions", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_questions(db, skip=skip, limit=limit)

@router.post("/submit", response_model=schemas.Assessment)
async def submit_assessment(
    assessment_data: schemas.AssessmentSubmit,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    total_score, categories_summary, incorrect_answers = 0, {}, []
    for answer_data in assessment_data.answers:
        option = crud.get_option(db, option_id=answer_data.selected_option_id)
        if not option: continue
        question = crud.get_question(db, question_id=answer_data.question_id)
        if not question: continue
        total_score += option.points
        category = question.category
        if category not in categories_summary:
            categories_summary[category] = {'score': 0, 'total': 0}
        max_points = crud.get_max_points_for_question(db, question.id)
        categories_summary[category]['score'] += option.points
        categories_summary[category]['total'] += max_points
        if option.points == 0:
            incorrect_answers.append({"question": question.text, "selected_option": option.text})
    
    ai_feedback = await ai_analysis.generate_assessment_feedback(categories_summary, incorrect_answers)
    analysis_text = ai_feedback.get("performance_report", "Analysis not available.")
    suggestions = ai_feedback.get("course_suggestions", [])
    
    sanitized_analysis_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', analysis_text)
    suggestions_json = json.dumps(suggestions)

    email_service.send_assessment_report(email=current_user.email, report_markdown=sanitized_analysis_text, score=total_score)
    
    return crud.create_assessment(db, user_id=current_user.id, score=total_score, answers=assessment_data.answers, analysis=sanitized_analysis_text, suggestions=suggestions_json)

@router.get("/history", response_model=List[schemas.Assessment])
def get_assessment_history(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return db.query(models.Assessment).filter(models.Assessment.owner_id == current_user.id).order_by(models.Assessment.created_at.desc()).all()

@router.get("/latest", response_model=Optional[schemas.Assessment])
def get_latest_assessment(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    latest = db.query(models.Assessment).filter(models.Assessment.owner_id == current_user.id).order_by(models.Assessment.created_at.desc()).first()
    if latest:
        # Business logic to prevent re-showing the same result can be handled here
        # For now, we will not delete it to preserve history.
        pass
    return latest
