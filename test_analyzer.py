from analyzer import analyze_resume


jd = """
Looking for a Data Engineer with Python, SQL,
AWS, Spark and MongoDB skills.
"""


resume = """
Skills:
Python
Java
MongoDB
AWS

Projects:
AI based recommendation system.
"""


result = analyze_resume(jd, resume)

print(result)