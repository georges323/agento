import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from agento!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    model = os.environ.get("MODEL")

    if api_key == None:
        raise RunetimeError('missing api key!')

    if model == None:
        raise RunetimeError('missing model!')

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="A super basic AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    args = parser.parse_args()

    user_prompt = args.user_prompt

    print(f"User prompt: {user_prompt}")

    response = client.models.generate_content(
        model=model,
        contents=user_prompt
    )

    usage_metadata = response.usage_metadata

    if usage_metadata == None:
        raise RunetimeError("Something went wrong retrieving response!")
    
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
