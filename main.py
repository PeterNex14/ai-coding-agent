from config.config import MAX_ITERS
from functions.call_function import call_function
from functions.call_function import available_functions
import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from config.prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if api_key is None:
        raise ValueError("GEMINI_API_KEY is not set")

    parser = argparse.ArgumentParser(description="Gabriel's AI Agent Boot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    iteration = 0
    while True:
        iteration += 1
        if iteration > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
            
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Usage metadata is none")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    functions_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)

        if (
            not result.parts 
            or not result.parts[0].function_response 
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        functions_responses.append(result.parts[0])

    messages.append(
        types.Content(
            role="user",
            parts=functions_responses,
        )
    )
    


    


if __name__ == "__main__":
    main()
