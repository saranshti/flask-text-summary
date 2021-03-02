from flask import Flask, jsonify
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
import pyrebase

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/sum/<string:id>')
def sum(id):
    config = {
        "apiKey": "AIzaSyA7XXqb2iYWefv9hkw6kx1RTwLrj2Ryhw8",
        "authDomain": "flask-text-summary.firebaseapp.com",
        "databaseURL": "https://flask-text-summary-default-rtdb.firebaseio.com",
        "projectId": "flask-text-summary",
        "storageBucket": "flask-text-summary.appspot.com",
        "messagingSenderId": "932532063095",
        "appId": "1:932532063095:web:a6785822f1a095b86d2f72",
        "measurementId": "G-1PF1XEQE6B"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    use = id
    OT = db.child("User").child(use).child("Original Text").get()
    R = db.child("User").child(use).child("Ratio").get()
    text = OT.val()
    ratio = R.val()
    num = ratio/100
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = (token.text for token in doc)
    punctuation = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n'''
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_score ={}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens) * num)
    summary = nlargest(select_length, sentence_score, key=sentence_score.get)
    final_summary = [word.text for word in summary]
    summary =''.join(final_summary)
    result = {
        "Number": ratio,
        "Name": summary 
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True) 
