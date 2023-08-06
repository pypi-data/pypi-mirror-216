import argparse
import os
import sys
import string
import random
import requests
import logging
import colorlog
import subprocess
from concurrent.futures import ThreadPoolExecutor
from aicoder.AICoderFull import AICoderFull
from aicoder.AICoderPartial import AICoderPartial

# Logger setup
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))
logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Function to check if the current directory is a git repo
def is_git_repo():
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to generate a random string
def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Function to generate a full program
def full_generator(prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
    if os.path.isdir("generated"):
        os.system("rm -rf generated")
    aicoderfull = AICoderFull(prompt, api_key, github_token, model)
    aicoderfull.generate_program()

# Function to generate a file from templates
def file_generator(prompt: str, api_key: str, github_token: str, model: str, template_files: list, orig_branch: str, new_branch: str, repo_name: str):
    aicoderpartial = AICoderPartial(prompt, api_key, github_token, model)
    aicoderpartial.gen_file_from_templates(template_files, prompt, orig_branch, new_branch, repo_name)

# Function to enhance a file
def enhancer(prompt: str, api_key: str, github_token: str, model: str, file_path: str, orig_branch: str, new_branch: str, repo_name: str):
    aicoderpartial = AICoderPartial(prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, prompt, orig_branch, new_branch, repo_name)

# Function to add comments to a file
def add_comments(prompt: str, api_key: str, github_token: str, model: str, file_path: str, orig_branch: str, new_branch: str, repo_name: str):
    final_prompt = "Given some code, add useful comments to it inside the code to easily understand what it does."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, new_branch, repo_name)

# Function to check for security vulnerabilities in a file
def check_security(prompt: str, api_key: str, github_token: str, model: str, file_path: str, orig_branch: str, new_branch: str, repo_name: str):
    final_prompt = "Given some code, search for security vulnerabilities and potential backdoors on it and if any, create a new code fixing it (if possible). Return only the fixed code with the comments. If you changed anything, add at the end of the code comments explaining the changes."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, new_branch, repo_name)

# Function to optimize a file
def optimize_file(prompt: str, api_key: str, github_token: str, model: str, file_path: str, orig_branch: str, new_branch: str, repo_name: str):
    final_prompt = "Given some code, optimize it without loosing functionality. Return a code that keeping the same functionality and respecting the class and function names, it's more clean and beautiful, simple, don't have duplice code, don't have code smells and is more efficient if possible. "
    final_prompt += "Don't remove comments, just improve them if possible. If you cannot improve the code just return the same code. If you changed anything, add at the end of the code comments explaining the changes. "
    final_prompt += "Be careful with chunks of code that looks similar but aren't exactly the same, even if part of the code can be improved the different functionalities must be keeped."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, new_branch, repo_name)

# Function to fix bugs in a file
def fix_bugs(prompt: str, api_key: str, github_token: str, model: str, file_path: str, orig_branch: str, new_branch: str, repo_name: str):
    final_prompt = "Given some code and keeping the same functionality fix all the bugs in it. Also, don't remove comments, just improve them if possible."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, new_branch, repo_name)

# Function to add common arguments to a parser
def add_common_arguments(parser):
    parser.add_argument('--api-key', default=None, type=str, help='Input API key')
    parser.add_argument('--model', default="gpt-4", type=str, help='Model to use')
    parser.add_argument('--prompt', default=None, type=str, help='Input prompt. It can be string, a file path or a url.')

# Function to get repo name
def get_git_org_repo_name():
    command = ['bash', '-c', 'git config --get remote.origin.url | sed -nE \'s/.*github.com[:\/]([^\/]*)\/(.*)\.git/\\1\\/\\2/p\'']
    return subprocess.check_output(command).strip().decode()

# Main function
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")  # Create subparsers

    # Create subparsers
    full_generator_parser = subparsers.add_parser('full-generator', help='Generate a full program from the prompt.')
    file_generator_parser = subparsers.add_parser('file-generator', help='Generate a file based on others as templates.')
    file_enhancer_parser = subparsers.add_parser('file-enhancer', help='Enhance a file based on the given prompt.')
    file_commentor_parser = subparsers.add_parser('file-comments', help='Ask to add comments to a file.')
    file_security_parser = subparsers.add_parser('file-security', help='Ask to search security vulnerabilities and backdoors in a file.')
    file_optimizer_parser = subparsers.add_parser('file-optimizer', help='Ask to optimize a file in terms of clean code and efficiency.')
    file_bug_fixer_parser = subparsers.add_parser('file-bugfixer', help='Ask to fix bugs in a file.')

    # Add common arguments to each subparser
    for subparser in [full_generator_parser, file_generator_parser, file_enhancer_parser, file_commentor_parser, file_security_parser, file_optimizer_parser, file_bug_fixer_parser]:
        add_common_arguments(subparser)

    # Add specific arguments to each subparser    
    file_generator_parser.add_argument('--template-files', nargs='+', help='List of template files')
    file_generator_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_generator_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_generator_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_generator_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    file_enhancer_parser.add_argument('--path', type=str, help='Path to file to enhance')
    file_enhancer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_enhancer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_enhancer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_enhancer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    file_commentor_parser.add_argument('--path', type=str, help='Path to file or folder to add comments')
    file_commentor_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_commentor_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_commentor_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_commentor_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    file_security_parser.add_argument('--path', type=str, help='Path to file or folder to search vulnerabilities')
    file_security_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_security_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_security_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_security_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    file_optimizer_parser.add_argument('--path', type=str, help='Path to file or folder to optimize')
    file_optimizer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_optimizer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_optimizer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_optimizer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')

    file_bug_fixer_parser.add_argument('--path', type=str, help='Path to file or folder to fix bugs')
    file_bug_fixer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_bug_fixer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_bug_fixer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_bug_fixer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    # Parse arguments
    args = parser.parse_args()
    prompt = os.environ.get("INPUT_PROMPT") or (args.prompt if hasattr(args,"prompt") else None)
    api_key = os.environ.get("INPUT_API_KEY") or (args.api_key if hasattr(args,"api_key") else None)
    model = os.environ.get("INPUT_MODEL") or (args.model if hasattr(args,"model") else None)

    if args.mode in ["file-generator", "file-enhancer", "file-comments", "file-security", "file-optimizer", "file-bugfixer"]:
        github_token = os.environ.get("GITHUB_TOKEN") or args.github_token
        orig_branch = os.environ.get("ORIGIN_BRANCH") or args.orig_branch
        to_branch = os.environ.get("TO_BRANCH") or args.to_branch
        repo_name = os.environ.get("GITHUB_REPOSITORY") or args.repo_name or get_git_org_repo_name()

        if args.mode == "file-generator":
            template_files = list(os.environ.get("TEMPALTE_FILES").split(",")) or args.template_files
                
        elif args.mode in ["file-enhancer", "file-comments", "file-security", "file-optimizer", "file-bugfixer"]:
            check_path = os.environ.get("CHECK_PATH") or args.path
    
    if not prompt and not args.mode in ["file-comments", "file-security", "file-optimizer"]:
        logger.error("Error: Missing prompt.")
        sys.exit(1)
    
    if not api_key:
        logger.error("Error: Missing API key.")
        sys.exit(1)
    
    # If prompt is file path, read it
    if prompt and os.path.isfile(prompt):
        logger.debug(f"Prompt read from {prompt}")
        with open(prompt, "r") as f:
            prompt = f.read()
    
    # If prompt is url, download it
    elif prompt and prompt.startswith("http"):
        logger.debug(f"Prompt downloaded from {prompt}")
        prompt = requests.get(prompt).text
    
    # If full generator mode
    if args.mode == 'full-generator':
        full_generator(prompt, api_key, github_token, model)
        exit(0)
    
    ### Checks for single file modifiers
    
    if not github_token:
        logger.warning("No Github token. PRs cannot be created automatically.")
    
    if github_token and not is_git_repo():
        logger.error("Error: Current directory isn't a git repository. Stopping.")
        exit(1)
    
    if github_token and not orig_branch:
        logger.error("Error: No orig branch. PRs cannot be created automatically. Stopping.")
        exit(1)
    
    if github_token and not to_branch:
        logger.error("Error: No to branch. PRs cannot be created automatically. Stopping.")
        exit(1)
    
    if github_token and not repo_name:
        logger.error("Error: No repo name. PRs cannot be created automatically. Stopping.")
        exit(1)
    
    # If file enhancer mode
    elif args.mode == 'file-generator':
        file_generator(prompt, api_key, github_token, model, template_files, orig_branch, to_branch, repo_name)
        exit(0)
    
    # If file commentor mode
    elif args.mode in ['file-enhancer', 'file-comments', 'file-security', 'file-optimizer', 'file-bugfixer']:
        # pompt is optional for all these modes except file-enhancer
        if args.mode == 'file-enhancer':
            f = enhancer
        elif args.mode == 'file-comments':
            f = add_comments
        elif args.mode == 'file-security':
            f = check_security
        elif args.mode == 'file-optimizer':
            f = optimize_file
        elif args.mode == 'file-bugfixer':
            f = fix_bugs
        
        # Check if path is file or folder
        if os.path.isfile(check_path):
            logger.debug(f"Given path {check_path} is a file.")
            f(prompt, api_key, github_token, model, check_path, orig_branch, to_branch, repo_name)
        
        elif os.path.isdir(check_path):
            logger.debug(f"Given path {check_path} is a folder.")
            with ThreadPoolExecutor(max_workers=3) as executor:
                for root, dirs, files in os.walk(check_path):
                    for file in files:
                        logger.debug(f"Checking file: {check_path}")
                        executor.submit(f, prompt, api_key, github_token, model, os.path.join(root, file), orig_branch, to_branch, repo_name)
        exit(0)

    
if __name__ == "__main__":
    main()