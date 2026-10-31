# HireSense AI – AI-Powered Resume Analyzer & Candidate Ranking System

HireSense AI is an AI-powered recruitment assistant built using Python, Google Gemini API, and Telegram Bot API. It helps evaluate candidate resumes against job descriptions, generate ATS-style compatibility scores, identify skill gaps, and rank candidates based on their suitability for a role.

The project aims to simplify initial resume screening by turning unstructured resume information into structured, actionable recruitment insights.

## Features

- **Resume Parsing:** Extract text from PDF resumes.
- **Job Description Analysis:** Analyze job requirements and identify relevant candidate criteria.
- **AI-Powered Resume Evaluation:** Compare resumes against job descriptions using Google Gemini AI.
- **ATS-Style Scoring:** Generate candidate compatibility scores from 0–100.
- **Candidate Ranking:** Rank successfully analyzed candidates according to their ATS scores.
- **Skill Matching:** Identify matched and missing skills.
- **Strengths & Weaknesses:** Generate candidate-specific evaluation insights.
- **Improvement Suggestions:** Recommend relevant projects, skills, and technologies.
- **Interview Preparation:** Generate role-specific interview questions.
- **Multiple Resume Uploads:** Evaluate multiple candidates against the same job description.
- **Duplicate Upload Protection:** Prevent repeated uploads of the same Telegram document.
- **Telegram Integration:** Interact with the application through a Telegram bot.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Generative AI | Google Gemini API |
| Bot Framework | python-telegram-bot |
| PDF Processing | PyMuPDF |
| API Integration | REST API, Requests |
| Environment Management | python-dotenv |
| Version Control | Git, GitHub |

## Project Structure

```text
HireSense-AI/
│
├── bot.py
├── analyzer.py
├── parser.py
├── prompts.py
├── test_analyzer.py
├── test_parser.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── uploads/       # Created locally for uploaded PDFs
```

## How It Works

1. The recruiter uploads a job description through Telegram.
2. Candidate resumes are uploaded as PDF documents.
3. The system extracts resume text.
4. Google Gemini AI evaluates each resume against the job description.
5. The system generates an ATS-style score and structured feedback.
6. Candidates are ranked according to their successful evaluation scores.
7. The recruiter receives the analysis and recommendations through Telegram.

## Candidate Evaluation

For each candidate, HireSense AI generates:

- ATS compatibility score
- Candidate match rating
- Matched skills
- Missing skills
- Strengths and weaknesses
- Project suggestions
- Recommended technologies
- Role-specific interview questions
- Hiring recommendation

The evaluation uses a weighted scoring framework:

| Evaluation Criteria | Weight |
|---|---:|
| Required Skills | 35% |
| Education & Qualifications | 15% |
| Relevant Experience | 20% |
| Projects & Practical Evidence | 20% |
| Other Job-Specific Requirements | 10% |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/tryphena413/HireSense-AI.git
cd HireSense-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project directory:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your `.env` file or expose API keys publicly.

### 5. Run the Telegram bot

```bash
python bot.py
```

## Telegram Bot Commands

| Command | Purpose |
|---|---|
| `/start` | Start the bot |
| `/upload_jd` | Upload a job description |
| `/upload_resume` | Upload candidate resumes |
| `/analyze` | Analyze and rank uploaded candidates |

## Sample Use Cases

- Compare multiple candidates against a single job description.
- Identify skill gaps in candidate resumes.
- Generate ATS-style compatibility scores.
- Rank candidates based on job relevance.
- Generate personalized interview questions.
- Support structured initial recruitment screening.

## Skills Demonstrated

- Python Programming
- Generative AI and Prompt Engineering
- Google Gemini API Integration
- REST API Integration
- Telegram Bot Development
- PDF Processing and Text Extraction
- Candidate Evaluation and Ranking
- Error Handling and Debugging
- Git and GitHub
- Problem Solving and Software Design

## Future Enhancements

- Support for multiple LLM providers.
- DOCX resume upload through Telegram.
- Resume validation and quality checks.
- Recruiter dashboard and analytics.
- Candidate comparison reports.
- Multi-language resume analysis.
- Cloud deployment and authentication.
- Advanced recruitment reporting.

## Author

**Sushmitha Hadassah Tryphena Chille**

GitHub: https://github.com/tryphena413

## Project Repository

https://github.com/tryphena413/HireSense-AI
