from flask import Flask, make_response, render_template, request, url_for
from flask_cors import CORS, cross_origin
from prompting.templates import generic_conversation
from controllers.firebase_wrapper import get_message_history, set_message_history, set_user_message


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


@app.route('/new_conversation', methods=['POST'])
def firebase_conversation():
    try:
        # pull necessary data from request
        data = request.get_json()
        user = data.get('user')
        assistant = data.get('assistant')
        user_persona = data.get('userPersona')
        assistant_persona = data.get('assistantPersona')
        sys_prompt = f'You are {assistant_persona}. You are are speaking to {user_persona}'
        count = data.get('count', 5)
        count = int(count)
        user_messages = [data.get('prompt')]

        data = get_message_history(assistant, user)
        user_messages.extend(data.get('user_messages', []))
        assistant_messages = data.get('assistant_messages', [])
        new_user_messages = []
        new_assistant_messages = []

    except Exception as e:
        print(e)
        return make_response({"error": "error parsing post"}, 400)

    try:
        # iterate through and generate conversation
        while count > 0:
            assistantCompletion = generic_conversation(
                sys_prompt, assistant_messages, user_messages)
            assistant_messages.append(assistantCompletion)
            new_assistant_messages.append(assistantCompletion)

            userCompletion = generic_conversation(
                sys_prompt,  user_messages, assistant_messages)
            user_messages.append(userCompletion)
            new_user_messages.append(userCompletion)
            count -= 1

        # update firebase
        set_message_history({
            "id": assistant,
            "persona": assistant_persona,
            "messages": new_assistant_messages,
        }, {
            "id": user,
            "persona": user_persona,
            "messages": new_user_messages,
        })

        return make_response({assistant: new_assistant_messages, user: new_user_messages}, 200)

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


if __name__ == '__main__':
    app.run()
