
import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.1-flash-lite"


def analyze_resume(jd_text, resume_text):

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from the .env file.")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
    )

    prompt = f"""
You are an expert Applicant Tracking System (ATS) and professional recruiter.

Analyze the candidate's resume against the supplied job description.

IMPORTANT:
- Support ALL industries and job roles, not just IT.
- Identify job requirements dynamically from the job description.
- Consider technical skills, professional skills, education,
  qualifications, experience, responsibilities and relevant projects.
- Compare actual resume evidence against each requirement.
- Do not assume skills or qualifications that are not mentioned.
- Do not invent experience, projects, achievements or certifications.
- Do not penalize candidates for requirements that are not applicable.
- Give specific and useful feedback.
- Do not edit or rewrite the resume.

SCORING:
1. Required skills: 35%
2. Education and qualifications: 15%
3. Relevant experience: 20%
4. Projects and practical evidence: 20%
5. Other job-specific requirements: 10%

Calculate an overall ATS score from 0 to 100 based on available evidence.

Return ONLY valid JSON in this exact structure:

{{
    "ats_score": 0,
    "rating": "",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "project_suggestions": [],
    "technology_recommendations": [],
    "interview_questions": [],
    "hiring_recommendation": ""
}}

Field instructions:
- matched_skills: Relevant skills and qualifications supported by the resume.
- missing_skills: Important job requirements not demonstrated.
- strengths: Actual strengths supported by resume evidence.
- weaknesses: Specific gaps or areas needing improvement.
- project_suggestions: Relevant projects or practical improvements.
- technology_recommendations: Technologies, tools or professional skills
  worth learning based on the job requirements.
- interview_questions: Generate 5 relevant questions for this role.
- hiring_recommendation: Choose "Recommended", "Consider",
  or "Needs improvement".

JOB DESCRIPTION:
{jd_text[:20000]}

CANDIDATE RESUME:
{resume_text[:20000]}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    try:
        # Retry temporary Gemini API errors up to 3 times.
        for attempt in range(3):

            response = requests.post(
                url,
                params={"key": GEMINI_API_KEY},
                json=payload,
                timeout=90
            )

            if response.status_code in [429, 500, 502, 503, 504]:

                if attempt < 2:
                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Gemini API temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

            response.raise_for_status()
            break

        response_data = response.json()

        ai_text = (
            response_data["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        result = json.loads(ai_text)

        score = int(result.get("ats_score", 0))
        score = max(0, min(100, score))

        result["ats_score"] = score
        result["rating"] = get_rating(score)

        # Ensure all expected fields exist.
        required_fields = {
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "project_suggestions": [],
            "technology_recommendations": [],
            "interview_questions": []
        }

        for field, default_value in required_fields.items():
            if not isinstance(result.get(field), list):
                result[field] = default_value

        if not isinstance(result.get("hiring_recommendation"), str):
            result["hiring_recommendation"] = "Consider"

        return result

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Gemini API connection failed: {error}"
        ) from error

    except (KeyError, IndexError, ValueError, TypeError) as error:
        raise RuntimeError(
            f"Could not process Gemini's analysis response: {error}"
        ) from error


def get_rating(score):

    if score >= 85:
        return "Excellent Match"

    elif score >= 70:
        return "Good Match"

    elif score >= 50:
        return "Average Match"

    else:
        return "Low Match"
