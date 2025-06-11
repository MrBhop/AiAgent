import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    if len(sys.argv) == 1:
        print("AI Code Assistant")
        print("\nUsage: python main.py <promp> [--verbose]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    output_verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if output_verbose:
        print("User prompt:", user_prompt)

    response = get_response(messages)

    if output_verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

def get_response(messages):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

if __name__ == "__main__":
    main()
