from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'hello world'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=6060)
