# 🎯 PATH.GPT — AI/ML Career Research Agent

> **An intelligent, personalized career research and roadmap agent for Computer Science students entering Artificial Intelligence and Machine Learning.**

---

## 📌 Problem Statement
For first- and second-year Computer Science Engineering students, breaking into AI/ML is often intimidating and confusing. Students frequently struggle with:
- **Information Overload:** Hundreds of tutorials, roadmaps, and buzzwords (LLMs, Diffusion, MLOps, Agents).
- **Prerequisite Anxiety:** Uncertainty about how much Calculus, Linear Algebra, or DSA is practically needed.
- **Generic Roadmaps:** Most online guides assume either a senior engineer or an advanced math PhD, ignoring a student's actual weekly study hours and current programming baseline.
- **Tutorial Hell:** Watching hours of videos without building resume-worthy, problem-solving projects.

---

## 💡 The Solution: PATH.GPT
**PATH.GPT** is a structured AI research agent built using the official **Google Gen AI SDK (`google-genai`)** and **Streamlit**. It acts as a senior academic and industry mentor that:
1. **Diagnoses Readiness:** Evaluates the student's current programming, AI, and math comfort.
2. **Recommends Matching Roles:** Suggests top 3 AI/ML roles (e.g., ML Engineer, Generative AI Engineer, Data Scientist) and explains *why* they fit the student.
3. **Conducts Skill Gap Analysis:** Segregates competencies into *Already Known*, *Need to Learn Urgently*, and *Learn Later*.
4. **Builds a Realistic 6-Month Roadmap:** Formulates a month-by-month and week-by-week curriculum tailored strictly to the student's available hours per week.
5. **Recommends High-Impact Projects:** Provides concrete project ideas with dataset recommendations and learning outcomes.
6. **Curates Authoritative Resources:** Recommends verified, official documentation and university courses (never hallucinated links).
7. **Interactive Follow-up Mentoring:** Features a contextual chat assistant that retains the student's profile context for targeted advice.

---

## 🏗️ Architecture & Data Flow

```text
[ Student Profile Form ]
         │
         ▼
[ Streamlit Web Frontend (app.py) ]
         │
         ▼
[ AI Service Layer (ai_service.py) ] ── (Loads GEMINI_API_KEY from .env securely)
         │
         ▼
[ Prompt Engineering & Grounding (prompts.py) ]
         │
         ▼
[ Google Gemini API via official google-genai SDK ] (gemini-3.5-flash-lite)
         │
         ▼
[ Structured Markdown Analysis & Roadmap ]
         │
         ▼
[ Rendered Dashboard + Markdown Export + Contextual Chat ]
```

---

## 🛠️ Technology Stack
- **Language:** Python 3.10+ (tested on Python 3.13)
- **AI Model / SDK:** Google Gemini API via official `google-genai` SDK
- **Frontend / UI:** Streamlit
- **Configuration & Security:** `python-dotenv`
- **Version Control Safety:** `.gitignore` shielding secrets

---

## 🔒 Security Best Practices
- **Never Hardcode Secrets:** The application strictly loads `GEMINI_API_KEY` from a local `.env` file via `python-dotenv`.
- **Git Shielding:** `.env` is listed in `.gitignore` to prevent any accidental commits or exposure to remote repositories.
- **Fail-Safe Startup:** If `GEMINI_API_KEY` is missing or invalid, the app halts gracefully with a friendly setup guide rather than crashing or printing environment dumps.
- **Zero-Trace Logging:** Keys are never echoed in terminal logs, UI elements, or error tracebacks.

---

## 🚀 Getting Started

### 1. Clone or Open the Repository
```powershell
cd "PATH-GPT-AIML"
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Edit `.env` and insert your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Verify Your Environment
Run the secure verification script:
```powershell
py check_env.py
```
*(Confirms key presence without exposing its characters).*

### 4. Install Dependencies
```powershell
py -m pip install -r requirements.txt
```

### 5. Launch the Application
```powershell
py -m streamlit run app.py
```
The application will launch in your browser at `http://localhost:8501`.

---

## 🎯 College Workshop Demonstration Guide

### 🎤 1-Minute Elevator Pitch
> *"Hello mentors and peers! As a first-year Computer Science student, one of the biggest challenges my friends and I face is figuring out how to navigate AI/ML without getting overwhelmed by jargon or tutorial hell.*
> 
> *To solve this, I built **PATH.GPT — AI/ML Career Research Agent**. Instead of generic chatbots, PATH.GPT diagnoses a student's actual background, programming comfort, and weekly available study hours. Powered by Google's Gemini API and the official `google-genai` SDK, it performs an in-depth readiness evaluation, pinpoints skill gaps, produces an actionable month-by-month 6-month roadmap, suggests resume-worthy projects, and offers follow-up mentoring.*
> 
> *It's designed with strict security best practices: zero hardcoded secrets, complete `.env` isolation, and a clean, workshop-ready Streamlit interface."*

### ❓ Anticipated Mentor Questions & Answers

**Q1: Why did you choose Google Gemini over other models?**
> **Answer:** Gemini's `gemini-3.5-flash-lite` delivers sub-second response latency, excellent reasoning capabilities for structured educational roadmaps, and generous free-tier API quotas ideal for student projects. Furthermore, Google's new unified `google-genai` SDK provides clean, native Python abstractions.

**Q2: What is an API and how does your app communicate with Gemini?**
> **Answer:** An API (Application Programming Interface) is a standardized messenger that allows our Python application to send instructions over HTTPS to Google's supercomputers and receive generated intelligence back. Our app packages the student's profile into a system-guided prompt, sends it to `generativelanguage.googleapis.com`, and deserializes the response into rich Markdown.

**Q3: How do you prevent API key leaks?**
> **Answer:** We adhere to the 12-factor app security methodology. The API key is stored exclusively in a local `.env` file that is ignored by Git via `.gitignore`. The code retrieves it through `os.getenv()`. Even in our verification scripts and error handlers, the key value is masked and never printed.

**Q4: How does PATH.GPT avoid hallucinating resources?**
> **Answer:** We enforce strict system instructions in `prompts.py` forbidding the model from inventing URLs or tool names. We explicitly constrain recommendations to authoritative domains such as official language documentation (python.org, pytorch.org), accredited university curricula (Stanford CS229, Fast.ai), and established platforms (Kaggle, GitHub).

**Q5: What are the current limitations and future improvements?**
> **Answer:**
> - *Current limitation:* Recommendations are statically scheduled over 6 months based on the student's initial input.
> - *Future improvement:* Add real-time GitHub repository analysis (inspecting a student's actual GitHub profile to auto-detect skills) and integrating Google Search Grounding for live job market trend analysis.

---

## 📄 License
This project is developed for educational and academic workshop demonstration purposes.
