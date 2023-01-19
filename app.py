from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import uuid
from predict_result import predict_result, load_saved_model

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LOAD MODEL ON APP START
ML_MODEL = load_saved_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.get('/')
def index_form():
    # SHOW IMAGE UPLOAD FORM
    return render_template('index.html')

@app.post('/')
def index_upload():
    error_msg = []
    if 'image_upload' not in request.files:
        error_msg.append('Image Not Uploaded')
        return render_template('index.html', errors = error_msg)
    
    file = request.files['image_upload']
    if file.filename == '':
        error_msg.append('No Selected File')
        return render_template('index.html', errors = error_msg)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = str(uuid.uuid4()) + '_' + filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('Saving Image at:', save_path)
        file.save(save_path)
        # Make prediction
        try:
            prediction_result = predict_result(save_path, ML_MODEL)
        except Exception as e:
            error_msg.append(str(e))
            return render_template('index.html', errors = error_msg)
        data = {
            'image_path': save_path,
            'filename': filename,
            'prediction_result': prediction_result
        }
        data['prediction_result']['probability'] = round(prediction_result['probability'] * 100, 2)
        print(data)
        return render_template('results.html', data = data)
    else:
        error_msg.append('Only png, jpg, jpeg images are allowed!')
        return render_template('index.html', errors = error_msg)