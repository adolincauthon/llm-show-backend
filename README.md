## Overview

This repo contains the code for the LLM-Show API. Currently prototyping HuggingFace and GPT4All models.

### Install

To install the required packages in a virtual environment run the following commands:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the program

I have included the launch.json file under the .vscode directory in order to run the program in debug mode. For debugging
run it using VS Code's debugger. Alternatively you can run server.py like a regular python program. The huggingface token will be read from the environment variable `HUGGING_TOKEN`

### Modifying

The backend code is located under server.py. Please modify the gpt4all route to get a response from GPT4All and return it in the given format. You will need to make some changes to demo.html or create a new html page in order to make this work.

### Prompt templates

Under the llm folder there is a file called templates.py. This is a module where we can create general prompt templates and interfaces with the API. This allows us to separate the prompting/llm client logic from our web app. In order to pull in a function to the server.py file, import it like this:

```
from llm.templates import generic_conversation

```
