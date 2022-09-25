import os
import hashlib
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import subprocess
from tasks import background_task
from dotenv import load_dotenv
from logger import log

load_dotenv(verbose=True)

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

DB_USER = os.getenv("DB_USER", None)
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_PORT = os.getenv("DB_PORT", None)
DB_NAME = os.getenv("DB_NAME", None)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 160 * 1000 * 1000
app.config["SECRET_KEY"] = DB_PASSWORD

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '': 
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename_hash = hashlib.md5(filename.encode('utf-8')).hexdigest()
            # Store filename_hash -> filename in the current session
            session["file"] = {"filename_hash": filename_hash, "filename": filename}
        else:
            return "Only .mp3, .wav or .flac files allowed"
        return redirect(url_for('upload_complete', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>AI Voice to text transcription &amp; translation</h1>
    <p>Simply upload your audio (mp3, wav or flac format), wait, and we'll email you the ai-powered transcription.</p>
    <p>Please be patient whilst your audio uploads, it is uploading there is simply no progress bar yet.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload-complete', methods=['GET', 'POST'])
def upload_complete():
    return f'''
    <!doctype html>
    <title>Translate / Transcribe File</title>
    <h1>Transcribe your audio file</h1>
    <a href="{ url_for('transcribe') }">Start Transcribing</a> 
    <h2>Transcribe <em>and</em> Translate my file into English</h2>
    (coming soon) <a href="{ url_for('transcribe') }">Start Transcribing and Translating</a> 
    '''

@background_task
def background_transcribe(app = None, filename = None):
    print(f"Running bg_transcribe on {filename}")
    subprocess.run(f"whisper uploads/{filename} --model medium", shell=True)


@app.route('/transcribe/', methods=['GET'])
def transcribe():
    """Transcribe audio"""
    filename = session.get("file")['filename']
    #subprocess.run(f"whisper uploads/{filename} --model medium --language English", shell=True)
    background_transcribe(filename=filename)
    return """<h1>Transcription started! We will send you the transcription when it is complete</h1>
            <p>Enter your email address to be contacted:</p>
            <form action='/alert' method='GET'>
              Email: <input type='email' name='email' /><br />
              <input type='submit' />
            </form>"""

@app.route('/translate/', methods=['GET'])
def translate():
    """Translate audio whilst transcribing it"""
    filename = session.get("file")['filename']
    return f'subprocess.run(f"whisper uploads/{filename} --model medium --language German --task translate")'

@app.route('/alert/', methods=['GET'])
def alert():
    return "<h1>Thank you. We'll email you the transcription once it is complete.</h1>"
