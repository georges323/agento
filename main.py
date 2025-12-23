import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERATIONS
from functions.call_functions import available_functions, call_function
from prompts import system_prompt


def main():
    print("Hello from agento!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    model = os.environ.get("MODEL")

    if api_key is None:
        raise RuntimeError('missing api key!')

    if model is None:
        raise RuntimeError('missing model!')

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="A super basic AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    user_prompt = args.user_prompt

    if args.verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    try:
        count = 0
        while count < MAX_ITERATIONS:
            final_response = generate_content(client, messages, model, args.verbose)
            if final_response:
                print('Final Response:')
                print(final_response)
                break
            count += 1
    except Exception as message:
        print(f'Error: {message}')

    if count == MAX_ITERATIONS:
        print(f"Max iterations {count} reached")

    sys.exit(1)

def generate_content(client, messages, model, verbose):
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if response.candidates is not None:
        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)

            usage_metadata = response.usage_metadata

            if usage_metadata == None:
                raise RuntimeError("Something went wrong retrieving response!")

            if verbose:
                print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
                print(f"Response tokens: {usage_metadata.candidates_token_count}")

            if response.function_calls is None or len(response.function_calls) == 0:
                return response.text

            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)

                if function_call_result.parts[0].function_response.response is None:
                    raise Exception('Error: Something went wrong calling the function')

                messages.append(types.Content(role="user", parts=function_call_result.parts))

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

if __name__ == "__main__":
    main()
