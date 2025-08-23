from flask import Flask, render_template, request, redirect, url_for, jsonify
import cohere
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

app = Flask(__name__)

# Home (login page)
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # (You can add authentication here later if needed)
    return redirect(url_for('chatbot'))

# Chatbot UI
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Chat API (updated for multiple languages)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    language = data.get('language', 'en')  # Default English if none selected

    try:
        # Tell Cohere to reply in selected language
        response = co.chat(
            message=f"Reply in {language} language: {user_message}",
            model="command-r"
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
