## Overview

This repo contains the code for the LLM-Show API. Currently prototyping HuggingFace and GPT4All as models.

### Install

To install the required packages in a virtual environment run the following commands:

```
python -m venv .venv
source .venv/env/bin/activate
pip install -r requirements.txt
```

### Running the program

I have included the launch.json file under the .vscode directory in order to run the program in debug mode. For debugging
run it using VS Code's debugger. Alternatively you can run server.py like a regular python program. If you go to your

### Modifying

The backend code is located under server.py. Please modify the gpt4all route to get a response from GPT4All and return it in the given format. You will
need to make some changes to demo.html or create a new html page in order to make this work.
