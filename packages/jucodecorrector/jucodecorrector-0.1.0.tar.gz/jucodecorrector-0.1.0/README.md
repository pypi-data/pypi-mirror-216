# Code Fixer for Jupyter Notebook


## Description
The Code Examiner and Corrector is a Python script designed to be used in Jupyter 
Notebook. It analyzes error code snippets and provides suggestions for correct code 
revisions. The script utilizes ChatGPT, an AI language model, to generate recommendations 
based on the given error message and context.

## Features
- Analyzes error code snippets and provides suggestions for code revisions.
- Utilizes the OpenAI GPT-3.5 language model for generating code recommendations.
- Helps improve code quality and assists in debugging errors.

## Requirements
- Jupyter Notebook
- Python 3.x
- OpenAI GPT-3.5 API credentials (see OpenAI documentation for details)
- Dependencies (install via pip):
    - jupyter_ai_magics
    - then in jupyter notebook %load_ext jupyter_ai_magics
    - openai
    - other dependencies as required

## Usage
1. Ensure you have set up the OpenAI API credentials by following the instructions in the 
documentation.
2. Install the package with pip or clone the repo
3. Open your jupyter notebook or jupyter lab file .ipynb
4. Import the class AiCodeFixer from the modul code_fixer_assistent. 
5. When error occures, call the function AiCodeCorrector().fix_broken_code() and review the 
recommendations and suggestions provided by ChatGPT.
6. Apply the recommended code revisions to fix errors and improve code quality.
7. Repeat the process for any additional error code snippets.


## Notes
- Ensure you have a stable internet connection to interact with the ChatGPT API.
- Be cautious when making changes to your code based on the suggestions provided. Verify the 
changes and test the code after revision.
- The effectiveness of the code suggestions and fixes depends on the quality of the error message 
and the complexity of the code.
- Experiment with different code snippets and variations to obtain the best results.

## Acknowledgments
- The code_fixer_assistent.py script utilizes the OpenAI GPT-3.5 language model. For more 
information about the language model and OpenAI API, visit the official OpenAI documentation.

