from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from point_tool import sort_points  # Import the Blueprint from point_tool.py
from number_tool import number_tool
from case_converter_tool import case_converter_tool
from text_formatter_tool import text_formatter_tool
from message_cleaner_tool import message_cleaner_tool
from make_pdf_copyable_tool import make_pdf_copyable_tool  # Import the Blueprint from make_pdf_copyable_tool.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp'

# Register the blueprints
app.register_blueprint(sort_points)
app.register_blueprint(number_tool)
app.register_blueprint(case_converter_tool)
app.register_blueprint(text_formatter_tool)
app.register_blueprint(message_cleaner_tool)
app.register_blueprint(make_pdf_copyable_tool)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/point-tool')
def point_tool():
    return render_template('point_tool.html')

@app.route('/number-tool')
def number_tool_route():
    return render_template('number_tool.html')

@app.route('/case-converter-tool')
def case_converter_tool_route():
    return render_template('case_converter_tool.html')

@app.route('/text-formatter-tool')
def text_formatter_tool_route():
    return render_template('text_formatter_tool.html')

@app.route('/message-cleaner-tool')
def message_cleaner_tool_route():
    return render_template('message_cleaner_tool.html')

@app.route('/add-periods-tool')
def add_periods_tool():
    return render_template('add_periods_tool.html')

@app.route('/remove-password', methods=['POST'])
def remove_password():
    # Your code here
    pass  # This is a placeholder, replace with the actual code

@app.route('/download-pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=False)
