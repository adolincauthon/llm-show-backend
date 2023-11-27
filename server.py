from flask import Flask, make_response, render_template, request, url_for
from flask_cors import CORS, cross_origin
from llm.templates import generic_conversation
from firebase_wrapper import get_message_history, set_user_message


app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['CORS_HEADERS'] = 'Content-Type,Access-Control-Allow-Origin'


# Route for getting demo page
@app.route('/', methods=['GET'])
def homepage():
    return render_template('demo.html')

# Route for hitting the huggingface API


@app.route('/conversation_api', methods=['POST'])
def conversation_api():
    try:
        # get data from POST request
        data = request.get_json()
        user_messages = data.get('userMessages')
        sys_prompt = data.get('sys_prompt')
        assistant_messages = data.get('assistantMessages')
        completion = generic_conversation(
            sys_prompt, user_messages, assistant_messages)
        resp = make_response({'generated_text': completion}, 200)
        return resp

    except Exception as e:
        return make_response({"error": "error parsing post"}, 500)


@app.route('/firebase_conversation', methods=['POST'])
def firebase_conversation():
    try:
        # pull necessary data from request
        data = request.get_json()
        user = data.get('user')
        assistant = data.get('assistant')
        userPrompt = user.get('prompt')
        assistantPrompt = assistant.get('prompt')
        userRef = data.get('userRef')
        assistantRef = data.get('assistantRef')
        messages = get_message_history(assistantRef, userRef)
        userMessages = messages.get('userMessages')
        assistantMessages = messages.get('assistantMessages')
        count = data.get('count', 5)
    except Exception as e:
        return make_response({"error": "error parsing post"}, 400)

    try:
        # iterate through conversation and update firebase records
        while count > 0:
            assistantCompletion = generic_conversation(
                assistantPrompt, assistantMessages, userMessages)
            assistantMessages.append(assistantCompletion)
            set_user_message(assistantRef, userRef, assistantCompletion)

            userCompletion = generic_conversation(
                userPrompt, assistantMessages, userMessages)
            userMessages.append(userCompletion)
            set_user_message(userRef, assistantRef, userCompletion)

        return make_response(200)

    except Exception as e:
        return make_response({"error": "Issue with huggingface client"}, 500)


# Route for hitting GPT4All
@app.route('/gpt4all', methods=['POST'])
def gpt4all():
    try:
        # Get data from GPT4all here and store the response in completion
        completion = ''
        # returns data to frontend
        resp = make_response({'generated_text': completion}, 200)
        return resp

    except Exception as e:
        return make_response({"error": "error parsing post"}, 500)


app.run()
