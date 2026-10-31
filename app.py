"""
PATH.GPT — AI/ML Career Research Agent
A high-impact, interactive AI career research platform for Computer Science students.
"""
import os
import streamlit as st
from dotenv import load_dotenv

from ai_service import AIService

# 1. Page Configuration
st.set_page_config(
    page_title="PATH.GPT — AI/ML Career Research Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Environment Variables & Service
load_dotenv()
api_service = AIService()

# 3. Premium CSS Styling for College Workshop & Competition Level UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E3A8A 100%);
        border-radius: 14px;
        padding: 2rem 2.2rem;
        color: #FFFFFF;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.25);
        border: 1px solid rgba(147, 197, 253, 0.4);
        color: #93C5FD;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        margin-bottom: 0.8rem;
    }
    
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
        background: linear-gradient(to right, #FFFFFF, #93C5FD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #CBD5E1;
        max-width: 800px;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 0.8rem;
    }
    
    .stat-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 0.05em;
    }
    
    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 0.2rem;
    }
    
    .stat-sub {
        font-size: 0.82rem;
        color: #2563EB;
        font-weight: 500;
    }
    
    .feature-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        height: 100%;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        border-color: #3B82F6;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)

# 4. Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "student_profile" not in st.session_state:
    st.session_state["student_profile"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "completed_milestones" not in st.session_state:
    st.session_state["completed_milestones"] = set()

# 5. Security & Key Check
if not api_service.is_configured():
    st.error("⚠️ **GEMINI_API_KEY is not configured!**")
    st.info(
        "To activate PATH.GPT, open your `.env` file in the project folder and insert your Gemini API key:\n\n"
        "```text\nGEMINI_API_KEY=your_key_here\n```\n\n"
        "*Your key remains safely on your computer and is never printed or sent anywhere else.*"
    )
    st.stop()

# 6. Sidebar: Student Profile Form
with st.sidebar:
    st.markdown("### 🎓 Student Profile")
    st.caption("Customize your background for a deeply personalized research report.")

    with st.form(key="profile_form"):
        display_name = st.text_input(
            "Name / Handle",
            placeholder="e.g., Alex",
            help="Personalizes your roadmap and certificate of preparation."
        )

        year_of_study = st.selectbox(
            "Academic Standing",
            options=[
                "1st Year B.Tech / BE (Foundation Phase)",
                "2nd Year B.Tech / BE (Core CS Phase)",
                "3rd Year B.Tech / BE (Internship Hunt)",
                "4th Year B.Tech / BE (Placement & Capstone)",
                "Master's / Graduate Student",
                "Career Switcher / Self-Taught"
            ],
            index=0
        )

        programming_skills = st.multiselect(
            "Programming Languages Known",
            options=["Python", "C / C++", "Java", "JavaScript", "SQL", "Go", "Rust", "None yet (Absolute Beginner)"],
            default=["Python"]
        )

        aiml_level = st.select_slider(
            "Current AI/ML Knowledge Level",
            options=[
                "Absolute Beginner (Starting from zero)",
                "Theoretical Concept (Watched tutorials/videos)",
                "Basic Practitioner (NumPy, Pandas, Scikit-Learn)",
                "Intermediate (Built Neural Nets in PyTorch/TF)"
            ],
            value="Absolute Beginner (Starting from zero)"
        )

        math_level = st.select_slider(
            "Mathematics & Statistics Comfort",
            options=[
                "High School Level (Need refresher)",
                "Basic Linear Algebra & Single-Variable Calculus",
                "Comfortable with Vectors, Probability & Matrices",
                "Advanced (Multivariate Calculus, SVD, Optimization)"
            ],
            value="High School Level (Need refresher)"
        )

        interests = st.multiselect(
            "Primary AI/ML Focus (Choose 1–4)",
            options=[
                "Machine Learning",
                "Deep Learning",
                "Generative AI & LLMs",
                "AI Agents & Automation",
                "Data Science & Analytics",
                "Computer Vision",
                "Natural Language Processing",
                "MLOps & Model Deployment"
            ],
            default=["Machine Learning", "Generative AI & LLMs"]
        )

        career_goal = st.selectbox(
            "Target Career Ambition",
            options=[
                "Land a Top AI/ML Summer Internship",
                "Become an AI/ML Engineer in Industry",
                "Become a Generative AI & Agent Engineer",
                "Become a Data Scientist",
                "Build AI Startups & SaaS Products",
                "Prepare for Master's / AI Research Labs"
            ]
        )

        weekly_hours = st.slider(
            "Available Study Time (Hours/Week)",
            min_value=4,
            max_value=35,
            value=12,
            step=1,
            help="Realistic consistency beats weekend cramming."
        )

        learning_style = st.selectbox(
            "Preferred Learning Methodology",
            options=[
                "Code-First: Build projects, learn concepts on the go",
                "Visual & Video: Fast-paced lectures & intuition diagrams",
                "Official Docs & Books: Deep dive into API references",
                "Math & Rigor: Proofs, equations, and foundational papers"
            ]
        )

        submit_button = st.form_submit_button(
            "🚀 Research & Generate My Roadmap",
            use_container_width=True
        )

    # Reset Action
    if st.button("🔄 Clear Profile & Restart", use_container_width=True):
        st.session_state["analysis_result"] = None
        st.session_state["student_profile"] = None
        st.session_state["chat_history"] = []
        st.session_state["completed_milestones"] = set()
        st.rerun()

# 7. Form Submission Handler
if submit_button:
    if not interests:
        st.sidebar.error("Please pick at least one AI focus area.")
    else:
        profile = {
            "name": display_name.strip() or "Student",
            "year_of_study": year_of_study,
            "programming_skills": programming_skills,
            "aiml_level": aiml_level,
            "math_level": math_level,
            "interests": interests,
            "career_goal": career_goal,
            "weekly_hours": weekly_hours,
            "learning_style": learning_style
        }
        st.session_state["student_profile"] = profile

        with st.spinner("🤖 PATH.GPT is researching career trajectories, mapping prerequisites, and formulating your 6-month roadmap..."):
            success, result = api_service.generate_career_analysis(profile)
            if success:
                st.session_state["analysis_result"] = result
                st.session_state["chat_history"] = []
                st.session_state["completed_milestones"] = set()
                st.toast("🎉 Career research and personalized roadmap generated!", icon="🎯")
            else:
                st.error(f"Generation error: {result}")

# 8. Main Stage Presentation
profile = st.session_state.get("student_profile")
analysis = st.session_state.get("analysis_result")

# Top Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✦ Powered by Google Gemini & GenAI SDK</div>
    <div class="hero-title">PATH.GPT</div>
    <div class="hero-subtitle">
        An intelligent career research & roadmap agent designed for engineering students. 
        Diagnose your readiness, eliminate tutorial paralysis, and build an industry-grade AI portfolio.
    </div>
</div>
""", unsafe_allow_html=True)

if not analysis:
    # Interactive Welcome & Feature Explorer
    st.markdown("### 🌟 Why PATH.GPT is Different")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 No Generic Roadmaps</h4>
            <p style="color: #64748B; font-size: 0.9rem;">
                Most roadmaps assume you already know multivariable calculus or have 40 hours a week. 
                PATH.GPT calculates an exact plan tailored to your actual schedule.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Truthful Skill Gap Diagnosis</h4>
            <p style="color: #64748B; font-size: 0.9rem;">
                Clear separation between what you already know, what you urgently need for your first project, 
                and advanced topics you can safely postpone.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class="feature-card">
            <h4>🚀 Day-by-Day Momentum</h4>
            <p style="color: #64748B; font-size: 0.9rem;">
                Includes a concrete <strong>Day 1 to Day 7 quickstart</strong> so you never sit staring at a blank screen wondering where to begin.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Career Paths Comparison Tool
    with st.expander("🔎 Quick Career Role Comparison (Click to Explore Roles)", expanded=False):
        st.markdown("Compare the most popular AI/ML career trajectories before submitting your profile:")
        tab1, tab2, tab3 = st.tabs(["Machine Learning Engineer", "Generative AI Engineer", "Data Scientist"])
        with tab1:
            st.markdown("""
            - **Focus:** Building, training, and deploying statistical models that predict or classify.
            - **Daily Tools:** Python, Scikit-learn, PyTorch, SQL, Docker, FastAPI.
            - **Best Suited For:** Students who love software engineering, clean code, and algorithms.
            """)
        with tab2:
            st.markdown("""
            - **Focus:** Building autonomous agents, LLM applications, RAG pipelines, and fine-tuning.
            - **Daily Tools:** Gemini API, LangChain/LlamaIndex, Vector DBs (Chroma/Pinecone), Prompt Engineering.
            - **Best Suited For:** Students excited by cutting-edge GenAI, rapid prototyping, and agentic systems.
            """)
        with tab3:
            st.markdown("""
            - **Focus:** Extracting business insights, hypothesis testing, data visualization, and predictive analytics.
            - **Daily Tools:** Pandas, Seaborn, SQL, Statistics, Scikit-learn, Tableau.
            - **Best Suited For:** Students who love data storytelling, statistics, and business problem solving.
            """)

    st.info("👈 **Get Started:** Fill in your student profile in the left sidebar and click **'Research & Generate My Roadmap'**!")

else:
    # 9. Active Student Dashboard Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Student Profile</div>
            <div class="stat-value">{profile.get('name', 'Student')}</div>
            <div class="stat-sub">{profile.get('year_of_study', '').split(' ')[0]} Year Engineering</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Primary Ambition</div>
            <div class="stat-value">{profile.get('career_goal', '').split(' ')[1] if len(profile.get('career_goal', '').split(' ')) > 1 else 'AI Career'}</div>
            <div class="stat-sub">{profile.get('interests', ['AI'])[0]}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Time Investment</div>
            <div class="stat-value">{profile.get('weekly_hours')} hrs/wk</div>
            <div class="stat-sub">{profile.get('weekly_hours', 10) * 24} hours across 6 mos</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Core Foundation</div>
            <div class="stat-value">{profile.get('programming_skills', ['Python'])[0]}</div>
            <div class="stat-sub">{profile.get('math_level', '').split(' ')[0]} Math</div>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Milestone Completion Tracker
    st.markdown("#### 🏆 Interactive 6-Month Milestone Tracker")
    st.caption("Check off monthly milestones as you complete them to track your journey toward internship readiness:")
    
    milestone_cols = st.columns(6)
    milestones = [
        "Month 1: Python & Math",
        "Month 2: Scikit-Learn",
        "Month 3: PyTorch & DL",
        "Month 4: Specialization",
        "Month 5: Deployment",
        "Month 6: Portfolio & Prep"
    ]
    
    for idx, (col, m_text) in enumerate(zip(milestone_cols, milestones)):
        with col:
            is_done = st.checkbox(m_text, key=f"m_check_{idx}")
            if is_done:
                st.session_state["completed_milestones"].add(idx)
            else:
                st.session_state["completed_milestones"].discard(idx)

    # Progress Bar Calculation
    progress_pct = len(st.session_state["completed_milestones"]) / 6.0
    st.progress(progress_pct, text=f"Roadmap Completion Progress: {int(progress_pct * 100)}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Download Dossier Button
    st.download_button(
        label="📥 Download Complete Research Dossier (.md)",
        data=analysis,
        file_name=f"PATH_GPT_Roadmap_{profile.get('name', 'Student')}.md",
        mime="text/markdown",
        help="Save this complete curriculum, projects, and interview guide to your machine."
    )

    st.divider()

    # Render Career Analysis in Organized Tabs
    st.markdown("### 📑 Detailed Career Research Report")
    
    # We display the rich formatted markdown report
    st.markdown(analysis)

    st.divider()

    # 10. Interactive AI Mentor Follow-up Chat
    st.markdown("### 💬 Ask PATH.GPT (Interactive Mentoring)")
    st.caption(f"Ask any follow-up question. PATH.GPT will answer while keeping your baseline ({profile.get('year_of_study')}, {profile.get('weekly_hours')} hrs/week) in mind.")

    # Smart Prompt Recommendation Chips
    st.markdown("**Quick questions you can ask:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    with qc1:
        if st.button("📌 What to code in Week 1?", use_container_width=True):
            quick_query = "What exact Python code exercise or mini-script should I write on Day 1?"
    with qc2:
        if st.button("⚖️ PyTorch vs TensorFlow?", use_container_width=True):
            quick_query = "For my career goal, should I prioritize PyTorch or TensorFlow, and why?"
    with qc3:
        if st.button("📐 How much Math do I need?", use_container_width=True):
            quick_query = "How much linear algebra and calculus do I practically need to understand before touching machine learning?"
    with qc4:
        if st.button("💼 How to land 1st internship?", use_container_width=True):
            quick_query = f"As a {profile.get('year_of_study')}, what is the single most important thing on my resume to get an AI internship interview?"

    # Render Existing Conversation
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Chat Input
    user_input = st.chat_input("Type your question for PATH.GPT...")
    final_query = quick_query or user_input

    if final_query:
        st.session_state["chat_history"].append({"role": "user", "content": final_query})
        with st.chat_message("user"):
            st.markdown(final_query)

        with st.chat_message("assistant"):
            with st.spinner("PATH.GPT is reviewing your profile and formulating guidance..."):
                chat_ok, chat_answer = api_service.ask_followup_question(profile, final_query)
                if chat_ok:
                    st.markdown(chat_answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": chat_answer})
                else:
                    err_msg = f"Sorry, I ran into an issue: {chat_answer}"
                    st.error(err_msg)
                    st.session_state["chat_history"].append({"role": "assistant", "content": err_msg})
