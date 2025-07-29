from sqlalchemy.orm import Session
import models, schemas

def populate_database(db: Session):
    questions_data = [
        {
            "text": "Percentage of marks (cumulative) in Intermediate (10+2)?",
            "category": "Academics",
            "options": [
                {"text": "Less than 40%", "points": 1},
                {"text": "40 to 60%", "points": 2},
                {"text": "61 to 79%", "points": 3},
                {"text": "80% or more", "points": 4}
            ]
        },
        {
            "text": "No. of external domain/technical certifications you have achieved?",
            "category": "Technical Skills",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "How equipped are you to work on an Accounting Software or ERP ?",
            "category": "Technical Skills",
            "options": [
                {"text": "Not aware of any Accounting software", "points": 1},
                {"text": "Partially equipped", "points": 3},
                {"text": "Fully equipped", "points": 5}
            ]
        },
        {
            "text": "How do you rate yourself in advanced Ms-Excel?",
            "category": "Technical Skills",
            "options": [
                {"text": "Poor", "points": 1},
                {"text": "Average", "points": 2},
                {"text": "Good", "points": 3},
                {"text": "Excellent", "points": 4}
            ]
        },
        {
            "text": "How much do you know about Accounts Receivable & Accounts Payable ?",
            "category": "Domain Knowledge",
            "options": [
                {"text": "Nothing", "points": 1},
                {"text": "Somewhat", "points": 3},
                {"text": "Proficient", "points": 5}
            ]
        },
        {
            "text": "Do you have knowledge to create structured financial models used in business planning & valuation?",
            "category": "Domain Knowledge",
            "options": [
                {"text": "No", "points": 1},
                {"text": "Learning still", "points": 3},
                {"text": "Yes", "points": 5}
            ]
        },
        {
            "text": "Are you well aware of the Indian Taxation Framework (knowledge of direct/indirect taxes, filing returns, etc)",
            "category": "Domain Knowledge",
            "options": [
                {"text": "Knowledge not required", "points": 1},
                {"text": "No", "points": 2},
                {"text": "Yes", "points": 5}
            ]
        },
        {
            "text": "No. of Non-technical (life skills) certifications you are familiar with?",
            "category": "Soft Skills",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "How good are you in verbal communication in English?",
            "category": "Communication",
            "options": [
                {"text": "Very Poor", "points": 1},
                {"text": "Poor", "points": 2},
                {"text": "Good", "points": 3},
                {"text": "Very Good/Excellent", "points": 4}
            ]
        },
        {
            "text": "How good are you in written communication in English?",
            "category": "Communication",
            "options": [
                {"text": "Very Poor", "points": 1},
                {"text": "Poor", "points": 2},
                {"text": "Good", "points": 3},
                {"text": "Very Good/Excellent", "points": 4}
            ]
        },
        {
            "text": "Name a book that has inspired you the most, and Why ?",
            "category": "Personality",
            "options": [
                {"text": "Text Answer", "points": 0} # Points for text answers are handled differently
            ]
        },
        {
            "text": "Number of tools you are familiar with?",
            "category": "Technical Skills",
            "options": [
                {"text": "zero", "points": 1},
                {"text": "1 to 3", "points": 2},
                {"text": "4 to 6", "points": 3},
                {"text": "More than 6", "points": 4}
            ]
        },
        {
            "text": "Have you ever taught your juniors or classmates?",
            "category": "Leadership",
            "options": [
                {"text": "No", "points": 1},
                {"text": "Planning in future", "points": 2},
                {"text": "Yes", "points": 3}
            ]
        },
        {
            "text": "Time spent on reading/watching Domain/Technology Magazines/Videos.",
            "category": "Learning",
            "options": [
                {"text": "Not interested", "points": 1},
                {"text": "Once in a while", "points": 2},
                {"text": "every week", "points": 3}
            ]
        },
        {
            "text": "Number of internships you have completed or enrolled so far ?",
            "category": "Experience",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "No. of projects independently or as part of CSR completed and successful ?",
            "category": "Initiative",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "Number of presentations have you given in Technical/Non Technical Events?",
            "category": "Communication",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "Have you done any certification in Business Analytics ?",
            "category": "Technical Skills",
            "options": [
                {"text": "No", "points": 1},
                {"text": "Yes", "points": 3}
            ]
        },
        {
            "text": "How often do you practice LRWS? (Listening, Reading, Writing, Speaking).",
            "category": "Communication",
            "options": [
                {"text": "Never", "points": 1},
                {"text": "Once in a while", "points": 2},
                {"text": "Daily", "points": 3}
            ]
        },
        {
            "text": "Number of workshops/seminars you attended?",
            "category": "Learning",
            "options": [
                {"text": "None", "points": 1},
                {"text": "One", "points": 2},
                {"text": "Two", "points": 3},
                {"text": "More than Two", "points": 4}
            ]
        },
        {
            "text": "Number of mock interviews you practiced and cleared successfully ?",
            "category": "Experience",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "How often do you make a to-do list and track tasks until completed ?",
            "category": "Organization",
            "options": [
                {"text": "Trust your memory", "points": 1},
                {"text": "Do not maintain list", "points": 2},
                {"text": "Once in a while", "points": 3},
                {"text": "Daily", "points": 4}
            ]
        },
        {
            "text": "How many awards or merit scholarships have you won so far ?",
            "category": "Academics",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "What kind of goals one should always focus on ?",
            "category": "Personality",
            "options": [
                {"text": "Don’t follow goals", "points": 1},
                {"text": "Short Term", "points": 2},
                {"text": "Long Term", "points": 3},
                {"text": "Both", "points": 4}
            ]
        },
        {
            "text": "Knowledge about AI and other technical tools is not really required in today's corporate world ?",
            "category": "Technical Skills",
            "options": [
                {"text": "True", "points": 1},
                {"text": "Not sure", "points": 2},
                {"text": "False", "points": 3}
            ]
        },
        {
            "text": "You have knowledge of how many AI Tools ?",
            "category": "Technical Skills",
            "options": [
                {"text": "0", "points": 1},
                {"text": "1", "points": 2},
                {"text": "2", "points": 3},
                {"text": "More than 2", "points": 4}
            ]
        },
        {
            "text": "How frequently are you engaged in a physical activity (like sports/gym/yoga/walking) ?",
            "category": "Wellness",
            "options": [
                {"text": "Never", "points": 1},
                {"text": "Once in a while", "points": 2},
                {"text": "Daily", "points": 3}
            ]
        },
        {
            "text": "How frequently do you eat street food or fast food ?",
            "category": "Wellness",
            "options": [
                {"text": "Daily", "points": 1},
                {"text": "Once in a while", "points": 2},
                {"text": "Never", "points": 3}
            ]
        },
        {
            "text": "Do you fall sick regularly?",
            "category": "Wellness",
            "options": [
                {"text": "Yes", "points": 1},
                {"text": "No", "points": 2}
            ]
        },
        {
            "text": "How many indoor games do you actively participate in regularly ?",
            "category": "Wellness",
            "options": [
                {"text": "None", "points": 1},
                {"text": "One", "points": 2},
                {"text": "More than one", "points": 3}
            ]
        },
        {
            "text": "Which of these do you practice to remain calm ?",
            "category": "Wellness",
            "options": [
                {"text": "Focus on work/None", "points": 1},
                {"text": "Talk less", "points": 2},
                {"text": "Read books", "points": 3},
                {"text": "Meditation", "points": 4}
            ]
        }
    ]

    for q_data in questions_data:
        question = models.Question(text=q_data["text"], category=q_data["category"])
        db.add(question)
        db.flush()  # Flush to get the question ID
        for o_data in q_data["options"]:
            option = models.Option(
                text=o_data["text"],
                points=o_data["points"],
                question_id=question.id
            )
            db.add(option)
    
    db.commit()
