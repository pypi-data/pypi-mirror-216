import argparse
import os
import sys
import string
import random
import requests

from time import sleep

from aicoder.AICoderFull import AICoderFull
from aicoder.AICoderPartial import AICoderPartial

def get_random_string(length):
    # With combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def full_generator(prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
    """Function that generates a program from nothing"""

    # Remove generated folder if it exists
    if os.path.isdir("generated"):
        os.system("rm -rf generated")

    aicoderfull = AICoderFull(prompt, api_key, github_token, model)
    aicoderfull.generate_program()

def file_generator(prompt: str, api_key: str, github_token: str, model: str, template_files: list, orig_branch: str, new_branch: str):
    """Function that generates a file from templates"""

    aicoderpartial = AICoderPartial(prompt, api_key, github_token, model)
    aicoderpartial.gen_file_from_templates(template_files, prompt, orig_branch, new_branch)

def enhancer(prompt: str, api_key: str, github_token: str, model: str, file_path: str, orig_branch: str, new_branch: str):
    """Function that generates a file using others as templates"""

    aicoderpartial = AICoderPartial(prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, prompt, orig_branch, new_branch)


def main():
    # Setup the argument parser
    parser = argparse.ArgumentParser()
    parser2 = argparse.ArgumentParser()

    # Mode
    parser.add_argument("mode", choices=["full-generator", "file-generator", "file-enhancer"], help="Mode of operation")

    # Add arguments for prompt, api_key, file_path and github_token
    parser.add_argument('--prompt', default=None, type=str, help='Input prompt. It can be string, a file path or a url.')
    parser.add_argument('--api-key', default=None, type=str, help='Input API key')
    parser.add_argument('--model', default="gpt-4", type=str, help='Model to use')
    
    args = parser.parse_args()
    prompt = os.environ.get("INPUT_PROMPT") or args.prompt
    api_key = os.environ.get("INPUT_API_KEY") or args.api_key
    model = os.environ.get("INPUT_MODEL") or args.model
    

    # Second round of arguments
    args2, github_token, template_files, modify_file_path, template_files, branch = None, None, None, None, None, None
    if args.mode == 'file-generator':
        parser2.add_argument('--template-files', nargs='+', required=True, help='List of template files')
        parser2.add_argument('--github-token', default=None, type=str, help='Github token')
        parser2.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
        parser2.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
        args2 = parser2.parse_args()
        
        github_token = os.environ.get("GITHUB_TOKEN") or args2.github_token
        template_files = args2.template_files
        orig_branch = args2.orig_branch
        to_branch = args2.to_branch
    
    elif args.mode == 'file-enhancer':
        parser2.add_argument('--file-path', required=True, type=str, help='Path to file to enhance')
        parser2.add_argument('--github-token', default=None, type=str, help='Github token')
        parser2.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
        parser2.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
        args2 = parser2.parse_args()
        
        github_token = os.environ.get("GITHUB_TOKEN") or args2.github_token
        modify_file_path = args2.file_path
        orig_branch = args2.branch
        to_branch = args2.to_branch

    if not prompt or not api_key:
        print("Error: Missing required inputs.")
        sys.exit(1)
    
    # If prompt is file path, read it
    if os.path.isfile(prompt):
        print(f"Prompt read from {prompt}")
        with open(prompt, "r") as f:
            prompt = f.read()
    
    # If prompt is url, download it
    if prompt.startswith("http"):
        print(f"Prompt downloaded from {prompt}")
        prompt = requests.get(prompt).text
    
    # If full generator mode
    if args.mode == 'full-generator':
        full_generator(prompt, api_key, github_token, model)
        exit(0)
    
    ### Checks for partial generators
    
    if not github_token:
        print("No Github token. PRs won't be created automatically.")
        sleep(3)
    
    if github_token and not orig_branch:
        print("Error: No orig branch. PRs won't be created automatically. Stopping.")
        exit(1)
    
    if github_token and not to_branch:
        print("Error: No to branch. PRs won't be created automatically. Stopping.")
        exit(1)

    # If file enhancer mode
    if args.mode == 'file-enhancer':
        enhancer(prompt, api_key, github_token, model, modify_file_path, orig_branch, to_branch)
        exit(0)
    
    # If file enhancer mode
    elif args.mode == 'file-generator':
        file_generator(prompt, api_key, github_token, model, template_files, orig_branch, to_branch)
        exit(0)

    
if __name__ == "__main__":
    main()