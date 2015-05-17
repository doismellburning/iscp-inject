from flask import *
import liberate
import os

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def upload_ui():
    return render_template('upload_ui.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]

    session = liberate.sign_in(username, password)
    
    uploaded_file = request.files['cameraInput']

    liberate.upload_course(session, filedata=uploaded_file.stream, filetype=uploaded_file.mimetype)

    print "Done!"

    return """Thanks"""
    

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=2223)
