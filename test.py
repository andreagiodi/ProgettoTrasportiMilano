#https://www.codespeedy.com/how-to-pass-javascript-variables-to-python-in-flask/
from flask import Flask, render_template, send_file, make_response, url_for, Response, request

app = Flask(__name__)

global value1
value1 = ''
global value2

@app.route('/')
def test():
    
    print(value1)
    return render_template('test1.html', value1=value1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)