from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, jsonify
import logging
import os

# Function to format the OCR text
import re

def format_ocr_text(ocr_text):
    # Define the strings after which line breaks should be added
    break_after_strings = ["المهام والمسؤوليات", "."]
    
    # Define keywords for different sections in Arabic
    keywords = {
        "Education": ["التعليم"],
        "Objective": ["الهدف الوظيفي"],
        "Experience": ["الخبرات العملية"],
        "Certificates": ["الشهادات"],
        "Technical Skills": ["المهارات التقنية"],
        "Personal Skills": ["المهارات الشخصية"],
        "Languages": ["اللغات"],
        # Add other sections if needed
    }
    
    # Split the text into lines
    lines = ocr_text.split('\n')
    
    # Use the first line as the name
    formatted_text = f"<strong>{lines[0]}</strong><br><br>"
    lines = lines[1:]
    
    # Iterate through the remaining lines
    for line in lines:
        # Check for contact information patterns
        email_pattern = re.compile(r'\S+@\S+\.\S+')
        phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')
        
        if email_pattern.search(line) or phone_pattern.search(line):
            formatted_text += f"{line}<br><br>"
        else:
            # Check for other keywords and format accordingly
            for section, section_keywords in keywords.items():
                if any(keyword in line for keyword in section_keywords):
                    formatted_text += f"<strong>{line}</strong><br><br>"
                    break
            else:
                formatted_text += line + '<br><br>'
    
    # Check for each string in break_after_strings and adjust line breaks
    for break_string in break_after_strings:
        # Replace the string with itself followed by two line breaks
        formatted_text = formatted_text.replace(break_string, break_string + '<br><br>')
    
    return formatted_text

# Setup blueprint
make_pdf_copyable_tool = Blueprint(
    'make_pdf_copyable_tool', __name__, template_folder='templates')

# Use absolute paths for the folders
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Ensure UPLOAD_FOLDER exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@make_pdf_copyable_tool.route('/make-pdf-copyable-tool')
def render_make_pdf_copyable_tool():
    return render_template('make_pdf_copyable_tool.html')

@make_pdf_copyable_tool.route('/make-pdf-copyable', methods=['POST'])
def make_pdf_copyable():
    if 'pdfFile' not in request.files:
        return jsonify({"status": "failed", "message": "No file part"})

    pdf_file = request.files['pdfFile']
    if pdf_file.filename == '':
        return jsonify({"status": "failed", "message": "No selected file"})

    # Secure the filename
    secure_pdf_filename = secure_filename(pdf_file.filename)
    pdf_file_path = os.path.join(UPLOAD_FOLDER, secure_pdf_filename)

    # Save the PDF file
    pdf_file.save(pdf_file_path)

    # Convert PDF to an image
    try:
        images = convert_from_path(
            pdf_file_path, 300, poppler_path=r'C:\poppler-23.08.0\Library\bin')
        image_path = os.path.join(UPLOAD_FOLDER, 'pdf_image.png')
        images[0].save(image_path, 'PNG')
    except Exception as e:
        logging.error("PDF to image conversion failed: %s", str(e))
        return jsonify({"status": "failed", "message": f"PDF to image conversion failed: {str(e)}"})

    # Perform OCR on the image
    try:
        ocr_text = pytesseract.image_to_string(Image.open(image_path), lang='ara')
      

        # Format the OCR text
        formatted_text = format_ocr_text(ocr_text)
        print("Formatted OCR Output:", formatted_text)
        logging.info("Formatted OCR Text: %s", formatted_text)
    except Exception as e:
        logging.error("OCR failed: %s", str(e))
        return jsonify({"status": "failed", "message": f"OCR processing failed: {str(e)}"})
    finally:
        # Clean up the uploaded files and generated images
        os.remove(pdf_file_path)
        os.remove(image_path)

    return jsonify({"status": "success", "message": formatted_text})
