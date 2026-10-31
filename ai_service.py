"""
ai_service.py — Service layer handling Gemini API calls using google-genai SDK.
Encapsulates communication, model configuration, and safe error handling.
"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from prompts import (
    SYSTEM_INSTRUCTION,
    CAREER_RESEARCH_PROMPT_TEMPLATE,
    FOLLOW_UP_CHAT_PROMPT_TEMPLATE,
)

# Load environment variables
load_dotenv()

# Active primary model
PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODELS = ["gemini-3.8-flash", "gemini-flash-latest"]


class AIService:
    """Manages AI career advising operations via Gemini API."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initializes the official google-genai client."""
        if not self.api_key or self.api_key.strip() in ("", "your_gemini_api_key_here", "my_key_here"):
            self.client = None
            return

        try:
            # 90 second timeout for thorough generation
            self.client = genai.Client(
                api_key=self.api_key,
                http_options=types.HttpOptions(timeout=90000)
            )
        except Exception as e:
            self.client = None
            print(f"[ERROR] Failed to initialize GenAI Client: {e}")

    def is_configured(self) -> bool:
        """Returns True if the API key and client are ready."""
        return self.client is not None

    def generate_career_analysis(self, profile: dict) -> tuple[bool, str]:
        """
        Generates a comprehensive AI/ML career research report and roadmap.
        Returns: (success: bool, content_or_error: str)
        """
        if not self.is_configured():
            return False, "Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file."

        # Format the research prompt with the student's profile details
        prompt = CAREER_RESEARCH_PROMPT_TEMPLATE.format(
            name=profile.get("name") or "Student",
            year_of_study=profile.get("year_of_study", "1st Year"),
            programming_skills=", ".join(profile.get("programming_skills", [])) or "None specified",
            aiml_level=profile.get("aiml_level", "Absolute Beginner"),
            math_level=profile.get("math_level", "Basic"),
            interests=", ".join(profile.get("interests", [])) or "Machine Learning",
            career_goal=profile.get("career_goal", "AI/ML Career"),
            weekly_hours=profile.get("weekly_hours", 10),
            learning_style=profile.get("learning_style", "Hands-on Projects")
        )

        models_to_try = [PRIMARY_MODEL] + FALLBACK_MODELS
        last_error = ""

        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )
                if response and response.text:
                    return True, response.text.strip()
            except APIError as e:
                last_error = f"Google API Error ({e.code}): {e.message}"
                if e.code == 404:
                    continue
                return False, last_error
            except Exception as e:
                last_error = f"Network or execution error: {str(e)}"
                continue

        return False, f"Could not generate career analysis. Details: {last_error}"

    def ask_followup_question(self, profile: dict, question: str) -> tuple[bool, str]:
        """
        Answers a follow-up question in the context of the student's profile.
        Returns: (success: bool, response_or_error: str)
        """
        if not self.is_configured():
            return False, "Gemini API key is not configured."

        prompt = FOLLOW_UP_CHAT_PROMPT_TEMPLATE.format(
            name=profile.get("name") or "Student",
            year_of_study=profile.get("year_of_study", "1st Year"),
            programming_skills=", ".join(profile.get("programming_skills", [])) or "None specified",
            aiml_level=profile.get("aiml_level", "Beginner"),
            math_level=profile.get("math_level", "Basic"),
            interests=", ".join(profile.get("interests", [])) or "Machine Learning",
            weekly_hours=profile.get("weekly_hours", 10),
            career_goal=profile.get("career_goal", "AI/ML Engineer"),
            user_question=question
        )

        try:
            response = self.client.models.generate_content(
                model=PRIMARY_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.6,
                )
            )
            if response and response.text:
                return True, response.text.strip()
            return False, "Received empty response from Gemini."
        except APIError as e:
            return False, f"Google API Error ({e.code}): {e.message}"
        except Exception as e:
            return False, f"Error: {str(e)}"
