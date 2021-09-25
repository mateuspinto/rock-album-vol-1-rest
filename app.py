from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
    return {'foo': request.form['foo']}


@app.route('/', methods=['PUT'])
def result2():
    return {'foo': 'Hello, World!'}
