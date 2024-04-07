
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    try:
        with open('/home/siddur/mysite/piped.html','r') as f:
            return f.read()
    except Exception as e:
        return str(e)

@app.route('/change', methods=('GET','POST'))
def change():
    if request.method == 'POST':
        with open('/home/siddur/mysite/piped.html','w') as f:
            f.write(str(request.form['text']))
            return "file: " + str(request.form['text'])
    return "NO POST"




