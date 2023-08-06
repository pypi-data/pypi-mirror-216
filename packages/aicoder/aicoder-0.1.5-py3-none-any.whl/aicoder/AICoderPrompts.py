


PERSONALITY = "You are a developer. The code you generate is beautiful, all commented, and very modular. You never leave TODOs or incomplete code and only respond with code."

PROGRAM_TO_GENERATE = """These are the specifications of the code you need to generate:\n\n"""

GET_ALL_FILES = """Return a valid json with all the file paths from the directory './generated/' that need to be created to generate the program.

The main file should be called 'main' with the extension (e.g. 'main.py'), it must contain the flow of the program so it should be the one importing from the rest.

The JSON must have this structure:
[
    {
        "path": "./generated/main.py",
        "description": "<This is a description of the content ./generated/main.py>",
        "dependencies": ["./generated/file2.h", "./generated/file3.py"]
    },
]

If needed don't forget headers '.h' and  implementations '.c, .cpp, .m'..."""


GET_FILE_CONTENTS = """These are the files we are generating for the program:\n
__FILES_JSON__

Return only the content that the file __FILE_PATH__ must have. Don't leave TODOs or incomplete code, write all the code of the file, and don't forget imports."""


FINAL_CLARIFICATIONS = """Return only code in the response. Remember to comment the code and don't leave TODOs or incomplete code. Do not add any extra information, markdown tags or apologies.
Do not include code fences in your response, for example
    
Bad response:
```javascript 
console.log("hello world")
```

Good response:
console.log("hello world")
"""

COMPILATION_COMMAND = """Respond exclusively with a JSON with a command to run to compile the program inside './generated/'.

The JSON must have this structure:

{
    "command": "<command to compile the program>"
}

If the program doesn't need to be compiled, put in the command an empty string.
Do not include anything but the JSON in the response.
"""

GET_ERRORS_JSON = """You have already generated the code for the program. You are going to be given the stderr from trying to compile the generated code for the program using the command: __COMMAND__
You need to organize which errors (don't care about warnings or notes) belongs to which files so they can be fixed later. Keep all the details (like code affected) from each error even if they are in other lines.
Respond with a valid json with all the errors by file path.

The JSON must have this structure:
[
    {
        "file_path": "./generated/file1.py",
        "errors_text": ["<First error text of the file1.py>", "<Second error text of the file1.py>"],
    },
]

If there are no errors, respond with an empty JSON: {}

These are the raw errors:

__RAW_ERRORS__"""


ERROR_FIX = """The file __FILE_PATH__ has the following errors: 
__ERROR_TEXT__

Please fix them and respond only with all the fixed file content, don't add apologies or explanations, just respond the full fixed code.

This is the current content of the file:
__FILE_CONTENT__"""


MODIFY_FILE = """Modify the file __FILE_PATH__ following this indications: __PROMPT__.
Respond only with final code of the file, don't add apologies or explanations, just respond the full code.

The file __FILE_PATH__ has the following content:

__FILE_CONTENT__
"""

FILE_FROM_TEMPALTES = """Develop the file __FINAL_FILE_PATH__ following this indications: __PROMPT__.
Respond only with final code of the file, don't add apologies or explanations, just respond the full code.

Please, use as templates the following files:
"""