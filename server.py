from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import audioConversion    
import bpm_calculate
import datetime

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/about')
def about():
    return "About Page"

@app.route('/audio', methods=['POST'])
def process_audio():
    data = request.get_data()
    data_length = request.content_length

    if (data_length > 1024 * 1024 * 10):
        return 'File too large!', 400

    # process data here:
    with open("upload_audio/test.m4a","wb") as file:
        print ("Processing data: ", data)
        file.write(data)   
    
    # convert_m4a_to_wav("test.wav", "test.wav"
    res=audioConversion.convert_m4a_to_wav("upload_audio/test.m4a", f"upload_audio/response_record-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.wav")
    if res is None:
        return json.dumps({ "text": "Error processing audio file!" }), 400
    
    fdata=bpm_calculate.process_audio_file(res);
    # print(fdata);

    
    return json.dumps({ "text": "Audio successfully processed!", "result": fdata }), 200








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
