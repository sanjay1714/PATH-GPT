"""
Stage 3: Minimal Gemini API request using google-genai SDK.
Goal: Verify end-to-end API connection and generate a simple test response.
"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

def run_gemini_test():
    # 1. Load the secret API key from our .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("[FAIL] GEMINI_API_KEY is missing from .env!")
        print("Please check your .env file before running.")
        return False

    print("[INFO] Initializing Google GenAI Client...")
    
    try:
        # 2. Create the Gemini client
        client = genai.Client(api_key=api_key)

        # 3. Define our simple Stage 3 test prompt
        test_prompt = "Explain machine learning in two simple sentences."
        print(f"[INFO] Sending test prompt to Gemini: \"{test_prompt}\"")
        
        # 4. Generate content using the recommended Gemini model
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=test_prompt,
        )

        # 5. Display the response safely
        print("\n" + "=" * 50)
        print("[SUCCESS] Gemini API Connection Verified!")
        print("=" * 50)
        print("\nGemini's Response:\n")
        print(response.text.strip())
        print("\n" + "=" * 50)
        return True

    except APIError as e:
        print(f"\n[ERROR] Google GenAI API Error: {e.message} (Status Code: {e.code})")
        return False
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_gemini_test()
    if not success:
        sys.exit(1)
