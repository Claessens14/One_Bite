
"""
# One Bite: We All Know The Rules (WIP) 

    *Coding without coding*

 - Long Files Only
 - Long Functions Only
 - Python Only
 - One Branch Only
 - Comments Everywhere
 - Install instuctions in the header 
 - LLM Does the coding
 - LLM does the fixes
    - *"In Opus we trust"* 🙏


## Setup
 - [ ] Get an anthropic claude key
 - [ ] Get an OpenI key
 - [ ] Paste them into the code

The reason for two models is incase one model gets stuck. 

(optional) use a virtual env for python
```
python3 -m venv venv && source venv/bin/activate
```

Mac: install `bat`, this is for syntax highlighting. 
```
brew install bat
```

python packages
```
pip install anthropic openai
```

Mac: add the utility to zsh path
```
pwd
echo "'aliass onebite=_GLOBAL_PATH_TO_PROGRAM_FILE'" >> ~/.zshrc
source ~/.zshrc
```

## Usuage
```
(ensure __your_file__ is in a unique git directory) 
onebite __file_name__.py
```

## ToDo

 - [ ] Add in wait bar for responses
 - [ ] Buttons 
    - `I` Implement (Writes to file)
    - `R` Run (Removes debugging) 
    - `S` Git commit `git add __file_name__.py && git commit -m "user message".` 
    - `M` Manual Edit `vim __file_name__.py`
    - `D` debug at line
    - `O` Toggle Open AI or Opus (Claude Opus / OpenAI GPT4 / Oblvious Opus / Obvious Open AI)
        - Oblvious means not aware of code or terminal output. 
    - `C` Clear Chat Memory.
    - `U` Discards the file changes `git restore __file_name__.py`

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
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("OPUS")
# Initialize the Anthropic client
anthropic_client = anthropic.Client(api_key=anthropic_api_key)

# Set the default model to OpenAI GPT
current_model = "openai"

def get_openai_response(conversation):
    """Get a response from OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Adjust model as needed
            messages=conversation
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, there was an issue with the OpenAI API."

def get_claude_response(conversation_text):
    """Get a response from Claude model."""
    try:
        response = anthropic_client.completion(
            prompt=conversation_text,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            max_tokens_to_sample=300,  # Adjust token limit as needed
            model="claude-2"  # Use desired Claude model
        )
        return response['completion'].strip()
    except Exception as e:
        print(f"Error with Claude API: {e}")
        return "Sorry, there was an issue with the Claude API."

def overwrite_file(file_name, content):
    """Overwrite a file with the given content."""
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"File '{file_name}' has been overwritten with new content.")

def commit_to_git(file_name, save_message):
    """Run git add and commit for the specified file."""
    try:
        subprocess.run(f'git add {file_name}', shell=True, check=True)
        subprocess.run(f'git commit -m "{save_message}"', shell=True, check=True)
        print(f"Changes to '{file_name}' committed with message: '{save_message}'")
    except subprocess.CalledProcessError as e:
        print(f"Error with git command: {e}")

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
    print("Welcome to the AI Chat! Type 'switch' to switch models, 'exit' to end the conversation.")
    conversation = []
    conversation_claude = []

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "switch":
            global current_model
            current_model = "claude" if current_model == "openai" else "openai"
            print(f"Switched to {current_model} model.")
            continue
        elif user_input.lower() == "run":
            # Run the file and optionally add the output to the next AI message
            file_output = run_python_file(file_name)
            continue

        # Combine file content with user input
        full_message = f"{file_content}\n\nUser Message:\n{user_input}"

        # Handle conversation differently for OpenAI GPT and Claude
        if current_model == "openai":
            # OpenAI requires a list of dictionaries for conversation
            conversation.append({"role": "user", "content": full_message})
            ai_reply = get_openai_response(conversation)
            print(f"OpenAI: {ai_reply}")
            # Append AI's reply to the conversation
            conversation.append({"role": "assistant", "content": ai_reply})

        elif current_model == "claude":
            # Claude requires a single string with human and AI prompts
            conversation_claude.append(f"{anthropic.HUMAN_PROMPT} {full_message} {anthropic.AI_PROMPT}")
            conversation_text = "".join(conversation_claude)
            ai_reply = get_claude_response(conversation_text)
            print(f"Claude: {ai_reply}")
            # Append AI's reply to the Claude conversation
            conversation_claude.append(ai_reply)

        # Check if the AI response should be written to the file
        save_prompt = input("Do you want to save this response to the file? (yes/no): ").strip().lower()
        if save_prompt == 'yes':
            overwrite_file(file_name, ai_reply)
            # Ask for a commit message
            save_message = input("Enter a commit message for git: ").strip()
            commit_to_git(file_name, save_message)

        # Optionally run the file and include output in next message
        run_prompt = input("Do you want to run the file and include its output in the next message? (yes/no): ").strip().lower()
        if run_prompt == 'yes':
            file_output = run_python_file(file_name)
            # Append the output to the next message to the AI
            file_content += f"\n\nExecution Output:\n{file_output}"

if __name__ == "__main__":
    # Argument parsing to specify a file path
    parser = argparse.ArgumentParser(description="AI Chat with OpenAI and Claude, with file content included in each message.")
    parser.add_argument("file", help="Path to the file to include in all messages")
    args = parser.parse_args()

    # Check if API keys are provided
    if not openai_api_key:
        print("Error: OpenAI API key is missing.")
    if not anthropic_api_key:
        print("Error: Anthropic API key is missing.")
    if openai_api_key and anthropic_api_key:
        openai.api_key = openai_api_key

        # Read the file content
        try:
            with open(args.file, 'r') as file:
                file_content = file.read()
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.")
            exit(1)

        # Start the chat with file content
        chat_with_ai(file_content, args.file)
    else:
        print("Please ensure both OpenAI and Anthropic API keys are set.")

