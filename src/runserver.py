import os
from flask import Flask
port = os.environ.get('PORT') or '8080'
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))