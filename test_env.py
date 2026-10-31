"""
Stage 2 Verification: Securely check for GEMINI_API_KEY without exposing it.
"""
import os
from dotenv import load_dotenv

def verify_environment():
    # Load variables from .env file into the system environment
    load_dotenv()

    # Retrieve the key
    api_key = os.getenv("GEMINI_API_KEY")

    # Safety check: Verify existence without printing any sensitive characters
    if not api_key:
        print("[FAIL] GEMINI_API_KEY was not found in .env")
        print("Please ensure your .env file contains: GEMINI_API_KEY=your_key_here")
        return False

    # Check that it is not the placeholder text
    if api_key.strip() in ("", "your_gemini_api_key_here", "my_key_here"):
        print("[FAIL] GEMINI_API_KEY is currently a placeholder. Please replace it with your actual key.")
        return False

    print("[SUCCESS] GEMINI_API_KEY is configured and detected successfully!")
    print(f"[SECURE CHECK] Key presence confirmed (length: {len(api_key)} characters). Key value remains hidden.")
    return True

if __name__ == "__main__":
    verify_environment()
