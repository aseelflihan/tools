import re
from flask import Blueprint, request, jsonify

message_cleaner_tool = Blueprint('message_cleaner_tool', __name__)

@message_cleaner_tool.route('/clean-messages', methods=['POST'])
def clean_messages():
    try:
        input_text = request.json.get('inputText', '')

        # Define a regular expression pattern to match the timestamp and sender name
        pattern = r"\[\d{2}-\w{3}-\d{2} \d{1,2}:\d{2} [APMapm]{2}\] [^:]+: "
        output_text = '\n'.join(re.sub(pattern, '', line) for line in input_text.splitlines())

        return jsonify({"status": "success", "outputText": output_text})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
