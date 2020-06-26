import os
from flask import Flask, render_template
port = os.environ.get('PORT') or '8080'
app = Flask(__name__, static_folder='static', static_url_path='')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/env")
def show_env_vars():
    return render_template('environ.j2',items=os.environ)

@app.route('/upload')
def upload_form():
	return render_template('upload.j2')

@app.route('/', methods=['POST'])
def upload_file():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))