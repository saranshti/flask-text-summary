from flask import Flask, jsonify
import spacy
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    nlp = spacy.load('en_core_web_sm')
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
