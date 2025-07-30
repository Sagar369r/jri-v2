# crud.py
# Corrected to work with the updated main.py and magic link authentication.

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
import json

import models, schemas, auth

# --- User Functions ---

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieves a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_or_create_user(db: Session, email: str) -> models.User:
    """
    Retrieves a user by email. If the user does not exist, a new one is created.
    """
    db_user = get_user_by_email(db, email=email)
    if db_user:
        return db_user
    new_user = models.User(email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_resume_data(db: Session, user_id: int, text: str, analysis: str, url: Optional[str]):
    """Updates the resume text, analysis, and URL for a given user."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.resume_text = text
        db_user.resume_analysis = analysis
        db_user.resume_url = url # Save the new URL
        db.commit()
        db.refresh(db_user)
    return db_user

# --- Magic Token Functions ---

def create_magic_token(db: Session, email: str, token_hash: str) -> models.MagicToken:
    """Stores a new magic link token hash in the database."""
    expires_at = datetime.utcnow() + timedelta(minutes=auth.MAGIC_LINK_EXPIRE_MINUTES)
    db_token = models.MagicToken(email=email, token_hash=token_hash, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def use_magic_token(db: Session, token_hash: str) -> Optional[models.MagicToken]:
    """Finds a magic token by its hash and marks it as used."""
    db_token = db.query(models.MagicToken).filter(models.MagicToken.token_hash == token_hash).first()
    if db_token:
        db_token.is_used = True
        db.commit()
        db.refresh(db_token)
        return db_token
    return None

# --- Question and Option Functions ---

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    """Retrieves a list of questions with their options."""
    return db.query(models.Question).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int):
    """Retrieves a single question by its ID."""
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def get_option(db: Session, option_id: int):
    """Retrieves a single option by its ID."""
    return db.query(models.Option).filter(models.Option.id == option_id).first()

def get_max_points_for_question(db: Session, question_id: int):
    """Calculates the maximum possible points for a given question."""
    result = db.query(func.max(models.Option.points)).filter(models.Option.question_id == question_id).scalar()
    return result or 0

# --- Assessment Functions ---

def create_assessment(db: Session, user_id: Optional[int], score: float, answers: List[schemas.AnswerSubmit], analysis: Optional[str] = None, suggestions: Optional[str] = None):
    """Creates a new assessment record for a user."""
    db_assessment = models.Assessment(score=score, owner_id=user_id, analysis=analysis, course_suggestions=suggestions)
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    
    for answer in answers:
        db_answer = models.Answer(assessment_id=db_assessment.id, question_id=answer.question_id, selected_option_id=answer.selected_option_id)
        db.add(db_answer)
    db.commit()
    
    return db_assessment

def get_assessment(db: Session, assessment_id: int):
    """
    Retrieves a single assessment by its ID.
    """
    return db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()

def update_assessment_analysis(db: Session, assessment_id: int, analysis: str, suggestions: str):
    """
    Updates an assessment record with the new AI analysis and suggestions.
    """
    db_assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if db_assessment:
        db_assessment.analysis = analysis
        db_assessment.course_suggestions = suggestions # Corrected field name
        db.commit()
        db.refresh(db_assessment)
    return db_assessment

def recalculate_assessment_details(db: Session, assessment: models.Assessment):
    """
    Recalculates the category summary and incorrect answers for an existing assessment.
    This is needed to generate the AI feedback.
    """
    categories_summary = {}
    incorrect_answers = []
    
    # --- FIX: Iterate directly over the assessment.answers relationship ---
    # The 'answers' attribute is a list of Answer objects, not a JSON string.
    for answer_data in assessment.answers:
        option_id = answer_data.selected_option_id
        question_id = answer_data.question_id

        option = get_option(db, option_id=option_id)
        if not option: continue
        
        question = get_question(db, question_id=question_id)
        if not question: continue

        category = question.category
        if category not in categories_summary:
            categories_summary[category] = {'score': 0, 'total': 0}
            
        max_points = get_max_points_for_question(db, question.id)
        categories_summary[category]['score'] += option.points
        categories_summary[category]['total'] += max_points
        
        if option.points == 0:
            incorrect_answers.append({"question": question.text, "selected_option": option.text})
            
    return categories_summary, incorrect_answers
