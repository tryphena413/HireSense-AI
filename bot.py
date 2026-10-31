
import os
import asyncio
from dotenv import load_dotenv

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


# ---------------- CONFIGURATION ----------------

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError(
        "TELEGRAM_TOKEN is missing. Please check your .env file."
    )


# ---------------- START COMMAND ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome to HireSense AI!\n\n"
        "I analyze resumes against a Job Description using AI.\n\n"
        "📄 Upload a JD using /upload_jd\n"
        "📑 Upload resumes using /upload_resume\n"
        "🔍 Analyze candidates using /analyze"
    )


# ---------------- UPLOAD COMMANDS ----------------

async def upload_jd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["upload_mode"] = "jd"

    await update.message.reply_text(
        "Please upload the Job Description PDF."
    )


async def upload_resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("jd"):
        await update.message.reply_text(
            "❌ Please upload a Job Description first using /upload_jd."
        )
        return

    context.user_data["upload_mode"] = "resume"

    await update.message.reply_text(
        "Please upload candidate resume PDFs."
    )


# ---------------- PDF UPLOAD HANDLER ----------------

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mode = context.user_data.get("upload_mode")

    if mode not in ("jd", "resume"):
        await update.message.reply_text(
            "First select an upload option:\n"
            "/upload_jd or /upload_resume"
        )
        return

    document = update.message.document
    file_name = os.path.basename(document.file_name or "document.pdf")

    os.makedirs("uploads", exist_ok=True)

    user_id = update.effective_user.id
    file_unique_id = document.file_unique_id

    # Prevent duplicate resume uploads.
    if mode == "resume":

        uploaded_ids = context.user_data.setdefault(
            "resume_file_ids", []
        )

        if file_unique_id in uploaded_ids:
            await update.message.reply_text(
                "⚠️ This resume has already been uploaded."
            )
            return

    # Give each uploaded file a unique filename.
    file_path = os.path.join(
        "uploads",
        f"{user_id}_{file_unique_id}.pdf"
    )

    file = await document.get_file()
    await file.download_to_drive(file_path)

    # -------- JOB DESCRIPTION --------

    if mode == "jd":

        jd_text = extract_text(file_path)

        if not jd_text or not jd_text.strip():

            await update.message.reply_text(
                "❌ Could not extract text from this PDF. "
                "Please try another PDF."
            )
            return

        # A new JD starts a new recruitment batch.
        context.user_data["jd"] = jd_text
        context.user_data["resumes"] = []
        context.user_data["resume_file_ids"] = []

        await update.message.reply_text(
            "✅ Job Description uploaded successfully!\n\n"
            "🧹 Previous candidate list cleared.\n\n"
            "Now use /upload_resume to upload candidate resumes."
        )

    # -------- RESUME --------

    else:

        resumes = context.user_data.setdefault("resumes", [])

        uploaded_ids = context.user_data.setdefault(
            "resume_file_ids", []
        )

        resumes.append(file_path)
        uploaded_ids.append(file_unique_id)

        count = len(resumes)

        await update.message.reply_text(
            f"✅ {file_name} uploaded successfully!\n"
            f"Total resumes uploaded: {count}\n\n"
            "Upload more resumes or type /analyze."
        )


# ---------------- ANALYZE RESUMES ----------------


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get resumes and remove duplicate file paths.
    resumes = list(dict.fromkeys(
        context.user_data.get("resumes", [])
    ))

    jd_text = context.user_data.get("jd")

    if not jd_text:
        await update.message.reply_text(
            "❌ Please upload a Job Description first using /upload_jd."
        )
        return

    if not resumes:
        await update.message.reply_text(
            "❌ No resumes uploaded.\n"
            "Use /upload_resume to upload candidate resumes."
        )
        return

    await update.message.reply_text(
        f"🔍 Analyzing {len(resumes)} unique resumes with Gemini AI..."
        " Please wait."
    )

    results = []
    errors = []

    for resume in resumes:

        try:
            # Extract resume text.
            resume_text = extract_text(resume)

            if not resume_text or not resume_text.strip():
                errors.append(
                    f"{os.path.basename(resume)}: No readable text found."
                )
                continue

            # Run Gemini without blocking Telegram.
            result = await asyncio.to_thread(
                analyze_resume,
                jd_text,
                resume_text
            )

            results.append((
                resume,
                result["ats_score"],
                result
            ))

        except Exception as error:
            errors.append(
                f"{os.path.basename(resume)}: {str(error)[:200]}"
            )

    if not results:
        message = (
            "❌ No resumes could be analyzed successfully.\n\n"
            + "\n".join(errors)
        )

        await update.message.reply_text(message[:4000])
        return

    # Rank candidates by ATS score.
    results.sort(
        key=lambda item: item[1],
        reverse=True
    )

    report = "📊 HireSense AI Candidate Ranking\n\n"

    for rank, (resume, score, result) in enumerate(results, start=1):

        report += f"""
🏆 Rank: {rank}

📄 Resume: {os.path.basename(resume)}

⭐ ATS Score: {score}%
📌 Rating: {result.get('rating', 'Not available')}

✅ Matched Skills:
{', '.join(result.get('matched_skills', [])) or 'None'}

❌ Missing Skills:
{', '.join(result.get('missing_skills', [])) or 'None'}

💪 Strengths:
{chr(10).join('- ' + item for item in result.get('strengths', [])) or 'None'}

⚠️ Weaknesses:
{chr(10).join('- ' + item for item in result.get('weaknesses', [])) or 'None'}

💡 Project Suggestions:
{chr(10).join('- ' + item for item in result.get('project_suggestions', [])) or 'None'}

📚 Recommended Technologies:
{', '.join(result.get('technology_recommendations', [])) or 'None'}

❓ Interview Questions:
{chr(10).join('- ' + item for item in result.get('interview_questions', [])) or 'None'}

🎯 Hiring Recommendation:
{result.get('hiring_recommendation', 'Not available')}

{'-' * 35}

"""

    # Report failed resumes separately.
    if errors:
        report += "\n⚠️ Some resumes could not be analyzed:\n"

        for error in errors:
            report += f"- {error}\n"

    # Send report in Telegram-friendly chunks.
    chunk_size = 3500

    for start_index in range(0, len(report), chunk_size):
        await update.message.reply_text(
            report[start_index:start_index + chunk_size]
        )

# ---------------- BOT SETUP ----------------

app = (
    Application.builder()
    .token(TOKEN)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .pool_timeout(30)
    .build()
)


# Register commands.

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("upload_jd", upload_jd_command))

app.add_handler(CommandHandler("upload_resume", upload_resume_command))

app.add_handler(
    MessageHandler(
        filters.Document.PDF,
        handle_pdf
    )
)

app.add_handler(CommandHandler("analyze", analyze))


# ---------------- START BOT ----------------

print("🚀 HireSense AI Bot is running...")

app.run_polling()
