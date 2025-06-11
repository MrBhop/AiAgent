import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT, MAX_ITERATIONS
from call_function import available_functions, call_function

def main():
    if len(sys.argv) == 1:
        print("AI Code Assistant")
        print("\nUsage: python main.py <promp> [--verbose]", "\n")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print("User prompt:", user_prompt, "\n")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    counter = 0
    while True:
        counter += 1

        if counter > MAX_ITERATIONS:
            print(f"Stopping after {MAX_ITERATIONS} iterations.", "\n")
            sys.exit(1)

        try:
            response = generate_content(client, messages, verbose)

            if response:
                print("Final response:")
                print(response, "\n")
                break
        except Exception as e:
            print(f"Error in generate_content: {e}", "\n")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count, "\n")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for call in response.function_calls:
        result = call_function(call, verbose)

        parts = result.parts
        if not parts or not parts[0].function_response:
            raise Exception("empty function call result")

        if verbose:
            print(f"-> {parts[0].function_response.response}", "\n")

        function_responses.append(parts[0])

    if not function_responses:
        raise Exception("no fuction responses generated. Exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
