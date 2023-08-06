import logging
import colorlog
import json
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from time import sleep
from AICoderPrompts import GET_ALL_FILES
from AICoder import AICoder, ALL_IMPORTS, IMPORTS_LOCK


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))

logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class AICoderFull(AICoder):
    """Class that generates code using OpenAI's API"""
    
    def __init__(self, prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
        super().__init__(prompt, api_key, github_token, model)
    

    def get_files_to_generate(self, extra_content=""):
        """Function that asks the model to return the file names to generate the program"""

        logger.info("Generating list of files...")
        msg = GET_ALL_FILES + extra_content
        files_to_generate = self.contact(msg)
        try:
            try:
                all_files = json.loads(files_to_generate)
            except json.decoder.JSONDecodeError as e:
                all_files = self.fix_json(msg, files_to_generate, str(e))
            
            # If more than 50% of files have .h extension, retry
            if len([file for file in all_files if file["path"].endswith(".h")]) > len(all_files) * 0.75 and len(all_files) > 3:
                logger.warning("Found more than 75% of .h files, retrying asking for the implementations...")
                extra_content = "\nLast time I asked your response was:\n" + files_to_generate
                extra_content += "\n\nDon't forget to include the implementation files."
                return self.get_files_to_generate(extra_content=extra_content)

            # If more than 50% of files have .m extension, retry
            if len([file for file in all_files if file["path"].endswith(".m")]) > len(all_files) * 0.75 and len(all_files) > 3:
                logger.warning("Found more than 75% of .m files, retrying asking for the headers...")
                extra_content = "\nLast time I asked your response was:\n" + files_to_generate
                extra_content += "\n\nDon't forget to include the header files"
                return self.get_files_to_generate(extra_content=extra_content)
            
            # If more than 50% of files have .c extension, retry
            if len([file for file in all_files if file["path"].endswith(".c")]) > len(all_files) * 0.75 and len(all_files) > 3:
                logger.warning("Found more than 75% of .c files, retrying asking for the headers...")
                extra_content = "\nLast time I asked your response was:\n" + files_to_generate
                extra_content += "\n\nDon't forget to include the header files."
                return self.get_files_to_generate(extra_content=extra_content)

            # If more than 50% of files have .cpp extension, retry
            if len([file for file in all_files if file["path"].endswith(".cpp")]) > len(all_files) * 0.75 and len(all_files) > 3:
                logger.warning("Found more than 75% of .cpp files, retrying asking for the headers...")
                extra_content = "\nLast time I asked your response was:\n" + files_to_generate
                extra_content += "\n\nDon't forget to include the header files."
                return self.get_files_to_generate(extra_content=extra_content)
            
            # Check if files are going to be generated in "./generated/"
            for f in all_files:
                if not "/generated/" in f["path"]:
                    logger.warning(f"Found a file not in './generated/' ({f['path']}). Asking to re-generate...")
                    extra_content = "\nLast time I asked your response was:\n" + files_to_generate
                    extra_content += "\n\nDon't forget to generate the files in the foler './generated/'"
                    return self.get_files_to_generate(extra_content=extra_content)
            
            print("Files to generate: ", json.dumps(all_files, indent=4))

            # Ask user if thats ok
            print("Is this ok? (Y/n)")
            user_input = input()
            if user_input.lower() in ["no", "n"]:
                print("I'll try to generate the files again... Tell me the problem:")
                extra_content = "\n" + input()
                return self.get_files_to_generate(extra_content=extra_content)
            
            return all_files
        except:
            raise Exception("The response is not a valid JSON: " + files_to_generate)


    def wait_on_dependencies(self, file: dict) -> str:
        """Function that waits until all the dependencies are generated"""

        dependencies_content = ""
        cont = 0
        all_exists = True
        while cont < 50:
            for dep in file["dependencies"]:
                if not os.path.exists(dep):
                    all_exists = False
                    logger.debug(f"Sleeping from {file['path']} the dependency: {dep}")
                    sleep(10)
                    if cont > 48:
                        logger.warning(f"The dependency {dep} of {file['path']} doesn't exist.")
                    cont += 1
                    continue
            if all_exists:
                break
        
        for dep in file["dependencies"]:
            if os.path.exists(dep):
                with open(dep, "r") as f:
                    dependencies_content += "\n\nThis is the content of the dependency file '" + file["path"] + "':\n" + f.read()
        
        return dependencies_content


    def generate_program(self):
        """Function that generates a full program from 0"""

        global ALL_IMPORTS

        # Get files to generate
        files_to_generate = self.get_files_to_generate()

        # Order files to generated from less amount of dependencies to more
        files_to_generate = sorted(files_to_generate, key=lambda x: len(x["dependencies"]))
        
        # Put the main file the first one and generate it now
        main_file_found = False
        for file in files_to_generate:
            if "/main." in file["path"].lower():
                logger.info("Generating main file...")
                main_file_content = self.generate_file(file, files_to_generate)
                files_to_generate.remove(file)
                file["description"] = file["description"] + "\nMain file content:\n" + main_file_content
                files_to_generate.insert(0, file)
                main_file_found = True
                break
        
        if not main_file_found:
            raise Exception("No main file found")
        
        # Initialize a ThreadPoolExecutor and a progress bar
        with tqdm(total=len(files_to_generate[1:]), desc="Generating files", unit="file") as pbar:
            sleep(0.1) #Allow the progress bar to be displayed
            with ThreadPoolExecutor(max_workers=3) as executor: # 3 is ok, don't oversaturate the server
                # Submit tasks to the executor
                futures = {executor.submit(self.generate_file, file, files_to_generate): file for file in files_to_generate[1:]}

                # As the futures complete, update the progress bar
                for future in concurrent.futures.as_completed(futures):
                    # Retrieve the file that this future was associated with
                    file = futures[future]

                    try:
                        # If the future completed without raising an exception,
                        # its result is returned by future.result()
                        future.result()
                    except Exception as exc:
                        logger.error(f"{file} generated an exception: {exc}")
                    else:
                        pbar.update(1)  # update progress bar

        # Try to compile the program
        self.try_to_compile()

        # Try to run the program
        self.try_to_run()
