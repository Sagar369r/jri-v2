# routers/assessment.py
from fastapi import APIRouter, Depends, HTTPException, status
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
    # This endpoint is now much faster. It only calculates the score and saves the answers.
    # The slow AI analysis has been removed.
    total_score = 0
    for answer_data in assessment_data.answers:
        option = crud.get_option(db, option_id=answer_data.selected_option_id)
        if option:
            total_score += option.points
    
    # Create the assessment record without analysis. Analysis will be generated on-demand.
    return crud.create_assessment(
        db, 
        user_id=current_user.id, 
        score=total_score, 
        answers=assessment_data.answers, 
        analysis=None, # Set analysis to None initially
        suggestions=None # Set suggestions to None initially
    )

@router.get("/history", response_model=List[schemas.Assessment])
def get_assessment_history(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return db.query(models.Assessment).filter(models.Assessment.owner_id == current_user.id).order_by(models.Assessment.created_at.desc()).all()

@router.get("/latest", response_model=Optional[schemas.Assessment])
def get_latest_assessment(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return db.query(models.Assessment).filter(models.Assessment.owner_id == current_user.id).order_by(models.Assessment.created_at.desc()).first()

# --- NEW ENDPOINT FOR ON-DEMAND AI ANALYSIS ---
@router.post("/{assessment_id}/analyze", response_model=schemas.Assessment)
async def analyze_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    # 1. Fetch the assessment from the database
    assessment = crud.get_assessment(db, assessment_id=assessment_id)
    if not assessment or assessment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    # 2. If analysis already exists, return it immediately
    if assessment.analysis:
        print(f"Analysis for assessment {assessment_id} already exists. Returning cached result.")
        return assessment

    # 3. If no analysis, generate it now (this is the slow part)
    print(f"Generating new analysis for assessment {assessment_id}...")
    categories_summary, incorrect_answers = crud.recalculate_assessment_details(db, assessment)
    
    ai_feedback = await ai_analysis.generate_assessment_feedback(categories_summary, incorrect_answers)
    analysis_text = ai_feedback.get("performance_report", "Analysis not available.")
    suggestions = ai_feedback.get("course_suggestions", [])
    
    sanitized_analysis_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', analysis_text)
    suggestions_json = json.dumps(suggestions)

    # 4. Update the assessment in the database with the new analysis
    updated_assessment = crud.update_assessment_analysis(
        db, 
        assessment_id=assessment_id, 
        analysis=sanitized_analysis_text, 
        suggestions=suggestions_json
    )
    
    # 5. Send the report email after analysis is complete
    email_service.send_assessment_report(
        email=current_user.email, 
        report_markdown=sanitized_analysis_text, 
        score=assessment.score
    )

    return updated_assessment
