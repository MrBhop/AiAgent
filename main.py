import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from call_function import available_functions, call_function

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

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    for call in response.function_calls:
        result = call_function(call, output_verbose)

        parts = result.parts
        if len(parts) > 0:
            response = parts[0].function_response.response
            print(f"-> {response}")

def get_response(messages):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        ),
    )

if __name__ == "__main__":
    main()
