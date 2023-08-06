import logging
from typing import List
import colorlog
import subprocess
import os
from github import Github
from .AICoderPrompts import MODIFY_FILE, FILE_FROM_TEMPALTES
from .AICoder import AICoder


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))

logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class AICoderPartial(AICoder):
    """Class that generates code using OpenAI's API"""
    
    def __init__(self, prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
        super().__init__(prompt, api_key, github_token, model)


    def modify_file(self, file_path: str, prompt: str, orig_branch: str, to_branch: str):
        """Function that generates a full program from 0"""

        if orig_branch:
            self.change_branch(orig_branch)

        # Prepare message
        logger.info(f"Modifying file {file_path}...")
        with open(file_path, "r") as f:
            file_content = f.read()
        msg = MODIFY_FILE.replace("__FILE_PATH__", file_path).replace("__PROMPT__", prompt).replace("__FILE_CONTENT__", file_content)

        # Get new content
        new_content = self.contact(msg)
        new_content = self.remove_fences(new_content)

        # Write new content
        with open(file_path, "w") as f:
            f.write(new_content)
        
        # If branch, create PR
        if orig_branch:
            commit_msg = f"File {os.path.basename(file_path)} modified by AICoder"
            commit_body = f"AICoder modified the file {file_path} according to this input:\n{prompt}"
            self.create_pull_request(commit_msg, commit_body, orig_branch, to_branch)


    def gen_file_from_templates(self, template_file_paths: List[str], final_file_path: str, prompt: str, orig_branch: str, to_branch: str):
        """Function that generates a file from a template"""

        if orig_branch:
            self.change_branch(orig_branch)

        # Create needed folders
        self.create_folder(final_file_path)

        # Prepare message
        logger.info(f"Generating {final_file_path} file from templates {', '.join(template_file_paths)}...")
        msg = FILE_FROM_TEMPALTES.replace("__FINAL_FILE_PATH__", final_file_path).replace("__PROMPT__", prompt)
        for f_path in template_file_paths:
            with open(template_file_paths, "r") as f:
                f_path_content = f.read()
                msg += f"\nThe template file {f_path} has the following content:\n\n{f_path_content}\n\n"
        
        # Get new content
        new_content = self.contact(msg)
        new_content = self.remove_fences(new_content)

        # Write new content
        with open(final_file_path, "w") as f:
            f.write(new_content)
        
        # If branch, create PR
        if orig_branch:
            commit_msg = f"File {os.path.basename(final_file_path[:46])} created by AICoder"
            commit_body = f"AICoder created the file {final_file_path} based on the files {', '.join(template_file_paths)} according to this input:\n{prompt}"
            self.create_pull_request(commit_msg, commit_body, orig_branch, to_branch)
    

    def change_branch(self, orig_branch: str):
        """Function that changes the branch"""

        # Check if the branch exists
        result = subprocess.run(["git", "rev-parse", "--verify", "--quiet", orig_branch], text=True, capture_output=True)

        # If the branch doesn't exist, create it
        if result.returncode != 0:
            subprocess.run(["git", "checkout", "-b", orig_branch], check=True)
        else:  # If the branch exists, just check it out
            subprocess.run(["git", "checkout", orig_branch], check=True)


    def create_pull_request(self, commit_message: str, commit_body: str, orig_branch: str, to_branch: str):
        """Function that creates a pull request"""

        github = Github(self.github_token)
        repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])

        # Commit changes to the new branch
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message[:70]], check=True)
        
        # Push the changes
        push_result = subprocess.run(["git", "push", "--set-upstream", "origin", orig_branch], text=True, capture_output=True)
        if push_result.returncode != 0:
            print("Failed to push the changes to the origin.")
            return

        # Create a pull request
        pr = repo.create_pull(
            title=commit_message,
            body=commit_body,
            head=orig_branch,
            base=to_branch
        )

        print(f"Pull request created: {pr.html_url}")
