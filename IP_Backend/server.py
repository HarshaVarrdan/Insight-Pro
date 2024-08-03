from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import functions

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        if not os.path.exists('temp'):
            os.makedirs('temp')
        filename = file.filename
        file_path = os.path.join('temp', filename)
        file.save(file_path)
        functions.setCsvFile(file_path)
        result = functions.GetNumericalValues.getNumericalColumns()
        os.remove(file_path)
        return jsonify({"result": result}),200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)