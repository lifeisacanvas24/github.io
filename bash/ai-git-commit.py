#!/usr/bin/env python3

import json
import logging
import os
import subprocess
from typing import List, Optional

import openai

# File paths
STARSHIP_LOGS = os.path.expanduser("~/.starship/logs")
CACHE_FILE = os.path.join(STARSHIP_LOGS, "ai-commit-cache")
FEEDBACK_LOG = os.path.join(STARSHIP_LOGS, "ai-commit-feedback.log")
LAST_RESPONSE_LOG = os.path.join(STARSHIP_LOGS, "last-openai-response.log")
REQUEST_LOG = os.path.join(STARSHIP_LOGS, "openai-request-payload.log")
STARTSHIP_STATUS_LOG = os.path.join(STARSHIP_LOGS, "ai-commit-status-starship.log")
API_KEY_PATH = os.path.expanduser("~/.ssh/openai-api-key")

'''# Available OpenAI models
MODEL_DESCRIPTIONS = {
    "gpt-3.5-turbo": "Fastest and most cost-effective model, good for most everyday tasks",
    "gpt-4": "More capable model, better for complex tasks and reasoning",
    "gpt-4-turbo": "Most advanced model, best for specialized and demanding applications",
}

DEFAULT_MODEL = "gpt-3.5-turbo"
MODEL = DEFAULT_MODEL
'''

# Create log directories if they don't exist
os.makedirs(STARSHIP_LOGS, exist_ok=True)

logging.basicConfig(
    filename=STARTSHIP_STATUS_LOG,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def safe_input(prompt, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            result = input(prompt)
            return result.strip()
        except EOFError:
            logging.error("End of file reached unexpectedly")
            continue
        except KeyboardInterrupt:
            logging.error("User interrupted")
            return None
        except Exception as e:
            logging.exception(f"Unexpected error occurred: {str(e)}")
            return None
    return None

def load_api_key():
    api_key_path = API_KEY_PATH
    if not os.path.exists(api_key_path):
        logging.error(f"API key file not found at {api_key_path}")
        raise FileNotFoundError(f"API key file not found at {api_key_path}")

    with open(api_key_path, 'r') as f:
        api_key = f.read().strip()

    if not api_key:
        logging.error("Empty API key file")
        raise ValueError("Empty API key file")

    return api_key

def get_staged_files() -> List[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting staged files: {e}")
        raise

def get_staged_changes_for_file(file_path: str) -> str:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting changes for file {file_path}: {e}")
        return ""

def get_commit_message_suggestions(prompt: str) -> List[str]:
    api_key = load_api_key()
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            top_p=1,
            n=5
        )
        return [choice['message']['content'] for choice in response['choices']]
    except Exception as e:
        logging.error(f"Error fetching suggestions: {str(e)}")
        return []

def prompt_user_for_input(suggestions: List[str]) -> Optional[str]:
    print("\nCommit message suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")

    while True:
        choice = safe_input("\nEnter the number of your preferred suggestion, or 'c' for custom: ")
        if choice.lower() == "c":
            return None
        try:
            num = int(choice)
            if 1 <= num <= len(suggestions):
                return suggestions[num - 1]
            else:
                print("Invalid selection. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number or 'c'.")

def commit_file(file_path: str, message: str) -> None:
    try:
        subprocess.run(["git", "commit", "-m", f"{file_path}: {message}"], check=True)
        logging.info(f"Successfully committed file: {file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to commit file {file_path}: {e}")

def get_diff():
    return subprocess.check_output(["git", "diff", "--staged"]).decode("utf-8")

def extract_comments_from_diff(diff_output):
    lines = diff_output.split("\n")
    comments = [
        line
        for line in lines
        if line.strip().startswith(("#", "//", "/*", "*/", "<!--", "--"))
    ]
    if comments:
        logging.info(f"Comments found: {' '.join(comments)}")
    else:
        logging.info("No comments found in the diff.")
    return " ".join(comments)

def log_request(prompt, model):
    with open(REQUEST_LOG, "w") as log_file:
        log_file.write(f"Model: {model}\nPrompt: {prompt}\n")

def log_response(response):
    with open(LAST_RESPONSE_LOG, "w") as log_file:
        log_file.write(json.dumps(response, indent=4))

def ai_git_commit():
    try:
        staged_files = get_staged_files()
        if not staged_files:
            logging.warning("No staged files found. Exiting.")
            return

        logging.info(f"Found {len(staged_files)} staged files")

        print("\nStaged files:")
        for i, file in enumerate(staged_files, start=1):
            print(f"{i}. {file}")

        selected_files = []
        custom_messages = {}

        for i, file in enumerate(staged_files, start=1):
            print(f"\nFile {i}: {file}")
            response = input("Do you want to commit this file? (y/n): ")
            if response.lower() == "y":
                selected_files.append(i)

                prompt = f"""Here's a summary of the changes for {file}:

{get_staged_changes_for_file(file)}

Please provide a brief description of the changes."""

                suggestions = get_commit_message_suggestions(prompt)
                selected_message = prompt_user_for_input(suggestions)

                if selected_message is None:
                    selected_message = safe_input(f"Please provide a custom commit message for {file}: ")

                custom_messages[file] = selected_message

        if not selected_files:
            logging.warning("No files selected for commit. Exiting.")
            return

        diff_output = get_diff()
        comments = extract_comments_from_diff(diff_output)
        logging.info(f"Comments found in the diff: {comments}")

        for file_index in selected_files:
            file = staged_files[file_index - 1]
            commit_file(file, custom_messages[file])
            logging.info(f"Successfully committed file: {file}")

        logging.info("All selected files committed successfully.")

    except EOFError:
        logging.error("End of file reached unexpectedly")
    except KeyboardInterrupt:
        logging.error("User interrupted")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    ai_git_commit()
