from flask import Blueprint, request, jsonify
import os
import PyPDF2
from werkzeug.utils import secure_filename

remove_password = Blueprint('remove_password', __name__)

@remove_password.route('/', methods=['POST'])
def remove_password_route():
    if 'pdfFile' not in request.files:
        return jsonify({"status": "failed", "message": "No file part"})
    pdf_file = request.files['pdfFile']
    if pdf_file.filename == '':
        return jsonify({"status": "failed", "message": "No selected file"})
    secure_pdf_filename = secure_filename(pdf_file.filename)
    pdf_file_path = os.path.join('temp', secure_pdf_filename)
    pdf_file.save(pdf_file_path)
    # ... (Add your existing PDF processing code here) ...
    return jsonify({"status": "success", "temp_file_path": 'decrypted_' + secure_pdf_filename})
