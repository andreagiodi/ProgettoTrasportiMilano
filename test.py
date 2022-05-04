#https://www.codespeedy.com/how-to-pass-javascript-variables-to-python-in-flask/
from flask import Flask, render_template, send_file, make_response, url_for, Response, request, jsonify
import json
app = Flask(__name__)

@app.route('/')
def testt():
    
    return render_template('test1.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)