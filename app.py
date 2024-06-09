from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

#API_KEY = 'Use your API Key'

os.environ["API_KEY"] = API_KEY
genai.configure(api_key=os.environ["API_KEY"])

genai.configure(api_key=os.environ["API_KEY"])
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_question', methods=['POST'])
def generate_question():
    topic = request.json['topic']
    if topic == 'Geography':
        prompt = 'Generate a simple and easy question about Geography.'
    elif topic == 'Sports':
        prompt = 'Generate a simple and easy question about Sports.'
    elif topic == 'Health':
        prompt = 'Generate a simple and easy question about Health.'
    else:
        return jsonify({'error': 'Invalid topic selected.'})

    try:
        response = model.generate_content(prompt)
        return jsonify({'question': response.text})
    except:
        return jsonify({'error': 'Failed to generate question. Unexpected response format from OpenAI API.'})

@app.route('/validate_answer', methods=['POST'])
def validate_answer():
    question = request.json['question']
    answer = request.json['answer']
    response = model.generate_content(
        f'this is the question "{question}" and the provied answer is this "{answer}".'
        ' so check if the answer is correct or incorrect just give one word '
        ' correct or incorrect.')
    print(response.text)
    return jsonify({'feedback': response.text})

if __name__ == '__main__':
    app.run(debug=True)
