import re


TECH_SKILLS = [
    "python",
    "java",
    "sql",
    "mongodb",
    "mysql",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "spark",
    "hadoop",
    "kafka",
    "react",
    "node",
    "express",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "rest api",
    "api",
    "data engineering"
]


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in TECH_SKILLS:
        if skill in text:
            found.append(skill)

    return found



def analyze_resume(jd_text, resume_text):

    jd_skills = extract_skills(jd_text)

    resume_skills = extract_skills(resume_text)


    matched = list(set(jd_skills) & set(resume_skills))

    missing = list(set(jd_skills) - set(resume_skills))


    if len(jd_skills) > 0:
        score = int((len(matched)/len(jd_skills))*100)
    else:
        score = 0



    return {

        "ats_score": score,

        "rating": get_rating(score),

        "matched_skills": matched,

        "missing_skills": missing,


        "strengths": [
            f"Candidate matches {len(matched)} required skills",
            "Technical keywords detected in resume",
            "Projects and certifications add value"
        ],


        "weaknesses": [
            f"Missing {len(missing)} important skills",
            "Need stronger project explanation"
        ],


        "project_suggestions": [
            "Add projects using missing technologies",
            "Explain architecture and scalability",
            "Mention tools, frameworks and results"
        ],


        "technology_recommendations": missing,


        "interview_questions": [
            "Explain your favorite project end-to-end",
            "How would you scale your application?",
            "Why did you choose this database?"
        ],


        "hiring_recommendation":
            "Recommended" if score >=70 else "Needs improvement"

    }




def get_rating(score):

    if score >=85:
        return "Excellent Match"

    elif score >=70:
        return "Good Match"

    elif score >=50:
        return "Average Match"

    else:
        return "Low Match"