
"""
Design principles: 
 - Pure functions because AI models are good at writing pure functions
 - Long files desired for easy use with LLMs
 - Chatting in the terminal

"""
import openai
import anthropic
import os
import argparse
import subprocess
from dotenv import load_dotenv
from tqdm import tqdm
import time

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("OPUS")

# Initialize Anthropic client
anthropic_client = anthropic.Client(api_key=anthropic_api_key)
current_model = "openai"

def get_openai_response(conversation, model="gpt-3.5-turbo"):
    """Get a response from OpenAI's updated API."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, there was an issue with the OpenAI API."

def get_claude_response(conversation_text):
    """Get a response from Claude model."""
    try:
        response = anthropic_client.completion(
            prompt=conversation_text,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            max_tokens_to_sample=300,
            model="claude-2"
        )
        return response['completion'].strip()
    except Exception as e:
        print(f"Error with Claude API: {e}")
        return "Sorry, there was an issue with the Claude API."

def overwrite_file(file_name, content):
    """Overwrite a file with the given content."""
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"File '{file_name}' has been overwritten.")

def commit_to_git(file_name, save_message):
    """Run git add and commit for the specified file."""
    try:
        subprocess.run(f'git add {file_name}', shell=True, check=True)
        subprocess.run(f'git commit -m "{save_message}"', shell=True, check=True)
        print(f"Changes to '{file_name}' committed with message: '{save_message}'")
    except subprocess.CalledProcessError as e:
        print(f"Error with git command: {e}")

def view_file_with_bat(file_name):
    """View the file with syntax highlighting using `bat`."""
    try:
        subprocess.run(f'bat {file_name}', shell=True)
    except FileNotFoundError:
        print("Error: 'bat' is not installed or not found in PATH.")

def progress_bar(seconds):
    """Display a progress bar for given seconds."""
    for _ in tqdm(range(seconds), desc="Processing...", ncols=100):
        time.sleep(1)

def run_python_file(file_name):
    """Run the specified Python file and capture the output."""
    try:
        result = subprocess.run(f'python {file_name}', shell=True, text=True, capture_output=True)
        print("File Output:", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running the file '{file_name}': {e}")
        return f"Error: {e}"

def chat_with_ai(file_content, file_name):
    print("Welcome to AI Chat! Type 'switch' to switch models, 'exit' to end.")
    conversation, conversation_claude = [], []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "switch":
            global current_model
            current_model = "claude" if current_model == "openai" else "openai"
            print(f"Switched to {current_model} model.")
            continue
        elif user_input.lower() == "view":
            view_file_with_bat(file_name)
            continue
        elif user_input.lower() == "run":
            file_output = run_python_file(file_name)
            continue

        # Combine file content with user input
        full_message = f"{file_content}\n\nUser Message:\n{user_input}"

        if current_model == "openai":
            conversation.append({"role": "user", "content": full_message})
            progress_bar(3)
            ai_reply = get_openai_response(conversation)
            print(f"OpenAI: {ai_reply}")
            conversation.append({"role": "assistant", "content": ai_reply})

        elif current_model == "claude":
            conversation_claude.append(f"{anthropic.HUMAN_PROMPT} {full_message} {anthropic.AI_PROMPT}")
            conversation_text = "".join(conversation_claude)
            progress_bar(3)
            ai_reply = get_claude_response(conversation_text)
            print(f"Claude: {ai_reply}")
            conversation_claude.append(ai_reply)

        if input("Save response to file? (yes/no): ").strip().lower() == 'yes':
            overwrite_file(file_name, ai_reply)
            save_message = input("Commit message: ").strip()
            commit_to_git(file_name, save_message)

        if input("Run file and include output in next message? (yes/no): ").strip().lower() == 'yes':
            file_output = run_python_file(file_name)
            file_content += f"\n\nExecution Output:\n{file_output}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Chat with OpenAI and Claude.")
    parser.add_argument("file", help="Path to the file to include in messages")
    args = parser.parse_args()

    if not openai_api_key:
        print("Error: OpenAI API key is missing.")
    if not anthropic_api_key:
        print("Error: Anthropic API key is missing.")
    if openai_api_key and anthropic_api_key:
        openai.api_key = openai_api_key

        try:
            with open(args.file, 'r') as file:
                file_content = file.read()
            chat_with_ai(file_content, args.file)
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.")
    else:
        print("Please ensure both API keys are set.")

