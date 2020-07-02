import os
import json
import logging
import clamd
from flask import Flask, render_template, redirect, request, flash
from azure.storage.blob import BlobServiceClient

# load the index json file
with open('index.json') as jsonfile:
    index = json.load(jsonfile)

# Create a Flask app
log_level = logging.DEBUG
logging.basicConfig(level=log_level)
port = os.environ.get('WEBSITES_PORT') or '8080'
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.environ.get('WEBSITE_AUTH_SIGNING_KEY') or "my secret key"

# connect to Azure storage
try:
    connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    azure_storage = True
except:
    app.logger.error("Unable to establish storage connection")
    azure_storage = False

if azure_storage:
    # get / create container
    try:
        container_client = blob_service_client.get_container_client("uploads")
    except:
        container_client = blob_service_client.create_container("uploads")

@app.route("/")
def hello():
    return render_template('text.j2',
        title="Home",
        index=index,
        text="""
This is a simple dockerized Python Flask web app used for testing purposes. It is not designed to be used in a production environment.
It solves two purposes:"
<ul><li>Testing of the complete CI/CD pipeline from building through to deployment</li>
<li>Integration with Azure (or other cloud platform)</li>
<li>Multi-container networking</li></ul>
</p><p>
The app is not designed to show best practice."""
    )

@app.route("/env")
def show_env_vars():
    return render_template('environ.j2',
        title="Environment",
        index=index,
        items=os.environ
    )

@app.route('/files')
def show_files():
	return render_template('files.j2',
        title="Files",
        index=index,
        file_list = container_client.list_blobs()
    )

@app.route('/upload')
def upload_form():
	return render_template('upload.j2',
        title="Files",
        index=index
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.warning("No file uploaded")
        flash('No file found in uploaded form')
        return redirect(request.url)

    upload_file = request.files['file']
    app.logger.info('File upload: %s', upload_file.filename)

    try:
        av = clamd.ClamdNetworkSocket("clamav-server")
    except:
        app.logger.error("Unable to establish network connection")
        flash('The AV server is unavailable. No uploads are being accepted until the server is back online.')
        return redirect(request.url)

    if av.ping() != 'PONG':
        app.logger.error("No Clam AV deamon responding")
        flash('The AV server is unavailable. No uploads are being accepted until the server is back online.')
        return redirect(request.url)

    result = av.instream(request.files['file'])['stream']
    app.logger.info("Upload scanned: %s - %s", result[0], result[1])

    if result[0] != 'OK':
        app.logger.warning("Virus detected in upload: %s", result[1])
        flash("Virus detected in upload: {}".format(result[1]))
        return redirect(request.url)

    blob_client = container_client.get_blob_client(upload_file.filename)
    blob_client.upload_blob(request.files['file'].read())

    return redirect("/files")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))