# ai_analysis.py
# This file contains the logic for generating insights using the Gemini AI model.

import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# --- UPDATED: More robust assessment feedback function ---
async def generate_assessment_feedback(categories_summary: dict, incorrect_answers: list) -> dict:
    """
    Generates a detailed performance report in Markdown and course suggestions as a separate JSON list.
    This is more robust than asking for a single complex JSON object.
    """
    # Prompt for the main analysis text
    analysis_prompt = """
    You are an expert career coach. Based on the following Job Readiness Index (JRI) assessment results, 
    provide a concise, encouraging, and actionable performance report in Markdown format. 
    The report must include these sections: '### Overall Summary', '### Key Strengths', '### Areas for Improvement', and '### Action Plan'.

    Here is the user's performance data:
    --- PERFORMANCE BY CATEGORY ---
    """
    for category, data in categories_summary.items():
        score = data.get('score', 0)
        total = data.get('total', 0)
        percentage = (score / total * 100) if total > 0 else 0
        analysis_prompt += f"- {category}: Scored {score:.1f} out of {total:.1f} ({percentage:.0f}%)\n"
        
    if incorrect_answers:
        analysis_prompt += "\n--- INCORRECTLY ANSWERED QUESTIONS ---\n"
        for item in incorrect_answers:
            analysis_prompt += f"- Question: {item['question']}\n  - Selected Answer: {item['selected_option']}\n"
    
    analysis_prompt += "\nGenerate the report now."

    try:
        # Generate the main report
        analysis_response = await model.generate_content_async(analysis_prompt)
        report_text = analysis_response.text

        # For now, we will return an empty list for course suggestions, 
        # as the main goal is to fix the analysis report.
        course_suggestions = []

        return {
            "performance_report": report_text,
            "course_suggestions": course_suggestions
        }
    except Exception as e:
        print(f"Error generating AI feedback: {e}")
        return {
            "performance_report": "We encountered an error generating your personalized feedback. The AI service may be temporarily unavailable.",
            "course_suggestions": []
        }


async def analyze_resume_text(resume_text: str) -> str:
    """Analyzes the provided resume text and returns feedback in Markdown."""
    prompt = f"""
    You are an expert resume reviewer for tech and business roles. Analyze the following resume text.
    Provide a concise, actionable critique in Markdown format. The report must include these sections:
    'Overall Impression', 'Strengths', 'Areas for Improvement', and 'Top 5 Keywords to Add'.

    --- RESUME TEXT ---
    {resume_text}
    --- END RESUME TEXT ---\n
    Generate the report now.
    """
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return "We encountered an error analyzing your resume. The AI service may be temporarily unavailable."

async def analyze_interview_conversation(question: str, answer_text: str) -> dict:
    """
    Analyzes a transcribed interview answer and provides both feedback and a relevant follow-up question.
    """
    prompt = f"""
    <Role>
    You are an AI Interview Chimera, a sophisticated coaching system embodying the combined expertise of a top-tier technical recruiter, a behavioral psychologist, and a master communicator. Your primary function is to conduct a realistic, challenging, and deeply insightful mock interview.
    </Role>

    <Context>
    You are in the middle of a live, voice-based mock interview for a technical role (like Software Developer, Data Analyst, or ML Engineer). You have just asked a question, and the user has responded with their spoken answer. Your task is to analyze their response and continue the conversation naturally.
    </Context>

    <Instructions>
    1.  **Analyze the User's Answer:** Critically evaluate the user's response to the question you asked. Assess its structure (e.g., STAR method), clarity, relevance, and impact. Identify both strengths and weaknesses.
    2.  **Provide Constructive Feedback:** Formulate a concise, encouraging, and actionable piece of feedback. DO NOT just say "You should use the STAR method." Instead, guide them by providing a concrete example. For instance, if they say "I fixed a bug," you might respond, "That's a solid start. To make that story even more powerful, you could quantify the result. For example, 'By implementing a caching strategy, I reduced the API response time by 300ms, which improved user satisfaction.'"
    3.  **Generate a Follow-up Question:** Based on the user's answer, formulate a logical and insightful follow-up question. This question should dig deeper into their response, challenge them to provide more detail, or pivot to a related competency. This is crucial for creating a realistic interview flow.
    4.  **Handle Conversational Input:** If the user's input is not a direct answer but a conversational phrase (e.g., "hello," "can you repeat that?"), respond naturally and steer the conversation back on track.
    </Instructions>

    <Constraints>
    - Your tone must be expert, supportive, and human-like.
    - Personalize all feedback based on the user's specific words. Avoid generic advice.
    - The entire response must be a single, valid JSON object.
    </Constraints>

    <Conversation_History>
    - AI's Question: "{question}"
    - User's Answer: "{answer_text}"
    </Conversation_History>

    <Output_Format>
    Return a single JSON object with two keys:
    1.  "feedback": "[A string containing your conversational feedback on the user's answer.]"
    2.  "next_question": "[A string containing your follow-up question.]"
    </Output_Format>
    """
    try:
        response = await model.generate_content_async(prompt)
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_text)
    except Exception as e:
        print(f"Error analyzing interview answer: {e}")
        return {
            "feedback": "I'm sorry, I encountered a technical issue. Let's try that again.",
            "next_question": question
        }
