from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/sum/<int:n>')
def sum(n):
    result = {
        "Number":n
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True) 