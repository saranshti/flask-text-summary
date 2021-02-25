from flask import Flask, jsonify
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
    return 'Hello, World!'

@app.route('/sum/<string:n>')
def sum(n):
    result = {
        "Number":n,
        "Name":"Saransh"
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True) 
