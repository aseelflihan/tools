from flask import Blueprint, request, jsonify

number_tool = Blueprint('number_tool', __name__)

@number_tool.route('/convert-number', methods=['POST'])
def convert_number():
    try:
        arabic_number = request.json.get('arabicNumber', '')
        english_number = arabic_number.translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789'))
        return jsonify({"status": "success", "englishNumber": english_number})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
