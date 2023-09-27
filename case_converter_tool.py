from flask import Blueprint, request, jsonify

case_converter_tool = Blueprint('case_converter_tool', __name__)

@case_converter_tool.route('/convert-case', methods=['POST'])
def convert_case():
    try:
        input_text = request.json.get('inputText', '')
        conversion_type = request.json.get('conversionType', '')

        if conversion_type == 'upper':
            output_text = input_text.upper()
        elif conversion_type == 'lower':
            output_text = input_text.lower()
        elif conversion_type == 'capitalized':
            output_text = input_text.title()
        else:
            return jsonify({"status": "failed", "message": "Invalid conversion type"}), 400

        return jsonify({"status": "success", "outputText": output_text})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
