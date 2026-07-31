import os
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv("TELEGRAM_TOKEN")

print("TOKEN:", TOKEN)

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from parser import extract_text
from analyzer import analyze_resume


# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

print("TOKEN:", TOKEN)


# Job Description
JD_TEXT = """
Looking for a Data Engineer.

Required Skills:
Python, SQL, AWS, MongoDB, Apache Spark, Data Engineering,
Machine Learning basics, REST APIs, Git.
"""


# ---------------- START COMMAND ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("START command received")

    await update.message.reply_text(
        "👋 Welcome to HireSense AI!\n\n"
        "I analyze resumes against a Job Description.\n\n"
        "📄 Upload multiple resumes and type /analyze"
    )



# ---------------- RESUME UPLOAD ----------------

async def handle_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📄 Resume received. Processing..."
    )


    file = await update.message.document.get_file()


    file_name = update.message.document.file_name


    file_path = f"uploads/{file_name}"


    await file.download_to_drive(file_path)



    # Store uploaded resumes

    if "resumes" not in context.user_data:
        context.user_data["resumes"] = []


    context.user_data["resumes"].append(file_path)


    count = len(context.user_data["resumes"])



    await update.message.reply_text(
        f"✅ {file_name} uploaded\n\n"
        f"Total resumes uploaded: {count}\n\n"
        "Upload more resumes or type /analyze"
    )



# ---------------- ANALYZE RESUMES ----------------

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):


    resumes = context.user_data.get(
        "resumes",
        []
    )


    if not resumes:

        await update.message.reply_text(
            "❌ No resumes uploaded.\nUpload resumes first."
        )

        return



    await update.message.reply_text(
        "🔍 Analyzing resumes... Please wait"
    )



    results = []



    for resume in resumes:


        # Extract resume text

        text = extract_text(resume)



        # Gemini analysis

        jd_text = context.user_data.get("jd")


if not jd_text:
    await update.message.reply_text(
        "❌ Upload Job Description first"
    )
    return


result = analyze_resume(
    jd_text,
    text
)



        results.append(
            (
                resume,
                result["ats_score"],
                result
            )
        )



    # Rank candidates

    results.sort(
        key=lambda x:x[1],
        reverse=True
    )



    report = "📊 HireSense AI Candidate Ranking\n\n"



    rank = 1



    for resume, score, result in results:


        report += f"""

🏆 Rank {rank}

📄 Resume:
{resume}

⭐ ATS Score:
{score}%

✅ Matched Skills:
{', '.join(result['matched_skills'])}

❌ Missing Skills:
{', '.join(result['missing_skills'])}

💡 Project Suggestions:
{', '.join(result['project_suggestions'])}

📚 Recommended Technologies:
{', '.join(result['technology_recommendations'])}

🎯 Recommendation:
{result['hiring_recommendation']}

-------------------------

"""


        rank += 1




    await update.message.reply_text(
        report
    )



# ---------------- BOT SETUP ----------------


app = Application.builder().token(TOKEN).build()



# Start command

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)



# Resume PDF upload

app.add_handler(
    MessageHandler(
        filters.Document.PDF,
        handle_resume
    )
)



# Analyze command

app.add_handler(
    CommandHandler(
        "analyze",
        analyze
    )
)



print("🚀 HireSense AI Bot is running...")



app.run_polling()

async def handle_jd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    file = await update.message.document.get_file()

    file_name = update.message.document.file_name

    jd_path = f"uploads/{file_name}"

    await file.download_to_drive(jd_path)


    jd_text = extract_text(jd_path)


    context.user_data["jd"] = jd_text


    await update.message.reply_text(
        "✅ Job Description uploaded successfully!\n\n"
        "Now upload candidate resumes."
    )