"""
Test ai_service.py functionality with a sample student profile.
"""
from ai_service import AIService

def test_service():
    service = AIService()
    if not service.is_configured():
        print("[FAIL] AIService is not configured with an API key.")
        return False

    print("[SUCCESS] AIService initialized successfully.")

    sample_profile = {
        "name": "Jordan",
        "year_of_study": "1st Year CSE",
        "programming_skills": ["Python", "C/C++"],
        "aiml_level": "Absolute Beginner",
        "math_level": "High School Math & Calculus",
        "interests": ["Machine Learning", "Generative AI"],
        "career_goal": "Become an AI/ML Engineer",
        "weekly_hours": 12,
        "learning_style": "Hands-on Projects & Coding"
    }

    print("[INFO] Testing generate_career_analysis call...")
    success, result = service.generate_career_analysis(sample_profile)
    if not success:
        print(f"[FAIL] Analysis failed: {result}")
        return False

    print("[SUCCESS] Career analysis generated successfully!")
    print(f"Generated text length: {len(result)} characters.")
    print("Preview:\n" + result[:250] + "...\n")

    print("[INFO] Testing ask_followup_question...")
    chat_success, chat_reply = service.ask_followup_question(sample_profile, "What should I learn first?")
    if not chat_success:
        print(f"[FAIL] Followup chat failed: {chat_reply}")
        return False

    print("[SUCCESS] Followup chat answered successfully!")
    print("Preview:\n" + chat_reply[:200] + "...\n")
    return True

if __name__ == "__main__":
    test_service()
