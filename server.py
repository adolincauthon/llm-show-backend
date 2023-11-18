from flask import Flask, make_response, render_template, request, url_for
from flask_cors import CORS, cross_origin
from huggingface_hub import InferenceClient


chat_model = 'HuggingFaceH4/zephyr-7b-beta'

app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['CORS_HEADERS'] = 'Content-Type,Access-Control-Allow-Origin'


@app.route('/', methods=['GET'])
def homepage():
    return render_template('demo.html')


@app.route('/conversation_api', methods=['POST'])
def conversation_api():
    try:
        hugging_client = InferenceClient(
            token="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")
        data = request.get_json()
        user_messages = data.get('userMessages')
        assistant_messages = data.get('assistantMessages')
        prompt = '<|system|> You are a greek philosopher. You like to engage in deep conversations and give meaningful responses. After each response you ask a new question. Your responses must be 4 sentences or less.</s>'
        for i in range(len(user_messages)):
            prompt += f'<|user|> {user_messages[i]}\n </s>'
            if i != len(user_messages) - 1:
                prompt += f'<|assistant|> {assistant_messages[i]}\n</s>'
        prompt += '<|assistant|> '
        print(prompt)
        completion = hugging_client.text_generation(
            prompt,  max_new_tokens=150, model=chat_model, return_full_text=False, temperature=.7)
        print(completion)
        resp = make_response({'generated_text': completion}, 200)
        return resp

    except Exception as e:
        return make_response({"error": "error parsing post"}, 500)


app.run()
