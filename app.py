from flask import Flask, render_template, request
import socket

app = Flask(__name__)

@app.route('/')
def home():
    myip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', ip = myip)

@app.route('/summary',methods = ['POST', 'GET'])
def summary():
    if request.method == 'POST':
        result = request.form
        movie_url = result.get('address')

    return render_template('summary.html', movie_url=movie_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)