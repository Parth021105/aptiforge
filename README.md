# AptiForge — Online Aptitude Practice & Assessment Platform ⚡

AptiForge is an online web-based Aptitude Practice & Assessment Platform built for students and faculty. It provides real-time AJAX question verification, progressive AI hint generation, timed mock exams with automated scoring, visual student analytics, and a comprehensive faculty administration portal.

---

## 🚀 Key Features

### 1. 🔐 Role-Based Authentication & Portals
- **Student Role**: Practice aptitude topics, receive 3-level progressive AI hints, take timed mock exams, and view performance analytics.
- **Faculty / Admin Role**: Upload question sets in bulk (CSV/JSON format), manually add/edit/delete questions, build custom mock exams, and monitor student score rosters.
- **1-Click Demo Login**: Pre-configured instant sign-in buttons for Student and Faculty review.

### 2. ⚡ Real-Time Practice Portal
- **Topic Filter Pills**: Filter questions across Quantitative Aptitude, Logical Reasoning, Verbal Ability, and Data Interpretation.
- **Instant Answer Checking**: Zero page reload AJAX validation with green/red highlight states and step-by-step solution explanations.
- **Practice Tracking**: Every attempt is logged in MongoDB to compute live topic accuracy stats.

### 3. ✨ Progressive AI Hint System
- **Level 1 (Concept)**: Identifies the core formula or mathematical rule.
- **Level 2 (Setup)**: Demonstrates the step-by-step problem setup.
- **Level 3 (Clue)**: Provides key calculation hints without spoiling the final answer choice.
- **Cloud AI API & Fallback**: Integrates with Groq API, OpenAI, or OpenRouter with an offline intelligent rule engine fallback.

### 4. ⏱️ Timed Mock Exam Engine
- **Live Countdown Timer**: Zero-padded mm:ss timer with flashing visual warnings when time gets low.
- **Interactive Question Palette**: Green (answered), grey (unanswered), cyan (current).
- **Instant Automated Scoring**: Immediate percentage score calculation, correct count, time spent, and itemized breakdown.

### 5. 📊 Visual Student Analytics
- **Summary Metrics**: Overall accuracy, average mock score, total tests completed, weak topic detection.
- **Topic Mastery Breakdown**: Color-coded progress bars for topic proficiency.
- **Focus Area Alerts**: Highlights topics under 65% accuracy with direct practice launch links.

### 6. ⚙️ Faculty / Admin Command Center
- **Question Uploader**: Drag-and-drop JSON/CSV file parser with column validation.
- **Question Bank Manager**: Filter, inspect, and delete questions from the database.
- **Mock Exam Builder**: Custom title, duration, question selection, and AI hint toggles.
- **Student Score Roster**: Overview of all student test submissions and performance metrics.

---

## 🛠️ Tech Stack & Directory Layout

- **Backend**: Python 3.10+, Flask, PyMongo / Flask-PyMongo, python-dotenv, requests
- **Database**: MongoDB (Local or MongoDB Atlas cloud via `MONGO_URI`)
- **AI Engine**: Cloud AI API (Groq, OpenAI, or OpenRouter) with intelligent fallback
- **Frontend**: Clean HTML5, Modern CSS3 Glassmorphic Styling, Vanilla JavaScript (Fetch API / AJAX)

```
aptiforge/
│── app.py                   # Flask server, route controllers & API endpoints
│── config.py                # App configuration & environment loaders
│── requirements.txt         # Project dependencies
│── .env.example             # Environment variable template
│── README.md                # Project documentation
│
├── database/
│   ├── db.py                # MongoDB connection handler & fallback logic
│   ├── models.py            # User, Question, Exam, Session, and Analytics models
│   └── sample_questions.json# Bundled 18+ sample aptitude questions
│
├── services/
│   └── ai_service.py        # Cloud AI & progressive hint generation engine
│
├── static/
│   ├── css/
│   │   └── style.css        # Glassmorphic dark design system styles
│   └── js/
│       ├── practice.js      # AJAX practice logic & AI hint fetching
│       ├── exam.js          # Timed exam ticker & score calculation
│       ├── analytics.js     # Topic accuracy bars & focus area alerts
│       └── admin.js         # CSV/JSON upload & exam builder logic
│
└── templates/
    ├── base.html            # Sticky layout, modern header & navbar
    ├── index.html           # Landing page
    ├── login.html           # Auth page with quick demo login buttons
    ├── dashboard_student.html # Student dashboard
    ├── dashboard_admin.html # Admin/Faculty command center
    ├── practice.html        # Question practice view
    ├── exam.html            # Timed mock exam view & report
    ├── analytics.html       # Performance analytics hub
    └── admin.html           # Faculty management panel
```

---

## ⚙️ Installation & Local Setup

### 1. Clone & Environment Setup
```bash
# Navigate to project directory
cd aptiforge

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```env
SECRET_KEY=aptiforge-super-secret-key-2026
MONGO_URI=mongodb://localhost:27017/aptiforge
AI_PROVIDER=groq
AI_API_KEY=your_groq_api_key_here
```

### 3. Run Application
```bash
python app.py
```
Open your browser at `http://localhost:5000`.

---

## 🎯 Presentation & Demo Instructions (For Review)

When presenting to faculty or evaluators:
1. **Quick Demo Login**: Click **Student Login** or **Faculty/Admin** on the `/login` screen to instantly sign in without typing passwords.
2. **Auto-Seeded Database**: The platform automatically seeds 18+ high-quality aptitude questions across Quantitative, Logical, Verbal, and Data Interpretation on initial startup.
3. **Showcase AI Hints**: Go to `/practice`, click **Level 1 (Concept)**, **Level 2 (Setup)**, or **Level 3 (Clue)** to show live progressive AI hint generation.
4. **Showcase Timed Exam**: Go to `/exam`, click **Start Test Now**, answer a few questions, and submit to demonstrate automated score generation and detailed itemized reports.
5. **Showcase Admin Capabilities**: Go to `/admin`, upload a CSV/JSON file or use the + Add Question modal to add a question live during the presentation.
