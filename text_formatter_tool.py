from flask import Blueprint, request, jsonify

text_formatter_tool = Blueprint('text_formatter_tool', __name__)

@text_formatter_tool.route('/format-text', methods=['POST'])
def format_text():
    try:
        input_text = request.json.get('inputText', '')
        action = request.json.get('action', '')

        if action == 'removeNewLine':
            output_text = ' '.join(input_text.splitlines())
        elif action == 'dotToNewLine':
            output_text = input_text.replace('.', '.\n')
        else:
            return jsonify({"status": "failed", "message": "Invalid action"}), 400

        return jsonify({"status": "success", "outputText": output_text})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
