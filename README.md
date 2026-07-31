HireSense AI
AI-Powered Resume Analyzer & Interview Assistant

HireSense AI is an intelligent recruitment assistant that analyzes resumes against job descriptions using Google Gemini AI, provides ATS-style matching, suggests improvements, and answers interview-related questions. The project helps job seekers evaluate their resumes and prepare effectively for technical interviews.

Features
Resume parsing from PDF and DOCX files
Job Description (JD) analysis
AI-powered resume evaluation using Google Gemini
ATS-style resume matching and scoring
Resume improvement suggestions
Interview question generation based on the JD
Telegram bot integration for easy interaction
Support for multiple resume uploads
Tech Stack
Category	Technologies
Language	Python
AI	Google Gemini API
Bot Framework	python-telegram-bot
Document Processing	PyMuPDF, python-docx
Data Processing	Pandas
Similarity Matching	RapidFuzz
Environment	python-dotenv
Version Control	Git & GitHub
Project Structure
HireSense-AI/
│
├── bot.py                 # Telegram bot entry point
├── parser.py              # Resume parsing module
├── analyzer.py            # Resume & JD analysis
├── prompts.py             # Gemini prompts
├── requirements.txt
├── README.md
├── .gitignore
│
├── uploads/
│   ├── resumes/
│   └── job_descriptions/
│
├── docs/
│   ├── architecture.png
│   └── workflow.png
│
└── screenshots/
    ├── bot_chat.png
    ├── ats_score.png
    └── recommendations.png
Workflow
Resume Upload
       │
       ▼
Document Parsing
       │
       ▼
Job Description Analysis
       │
       ▼
Google Gemini AI
       │
       ▼
Resume Matching
       │
       ▼
ATS Score
       │
       ▼
Suggestions & Interview Questions
       │
       ▼
Telegram Bot Response
Installation

Clone the repository:

git clone https://github.com/yourusername/HireSense-AI.git

Navigate to the project:

cd HireSense-AI

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GEMINI_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_bot_token

Run the bot:

python bot.py
Sample Use Cases
Analyze resumes against a job description
Generate ATS-style compatibility scores
Receive personalized resume improvement suggestions
Generate interview questions tailored to a specific role
Evaluate multiple resumes for recruitment support
Skills Demonstrated
Python Programming
Artificial Intelligence
Generative AI
Prompt Engineering
REST API Integration
Telegram Bot Development
Resume Parsing
File Handling
Data Processing
Software Design
Problem Solving
Future Enhancements
Support for multiple LLM providers
Multi-language resume analysis
Recruiter dashboard
Candidate ranking system
Analytics and reporting
Resume keyword optimization
Cloud deployment
Authentication and user management
License

This project is licensed under the MIT License.

Author
Sushmitha Hadassah Tryphena Chille
