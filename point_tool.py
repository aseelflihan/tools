from flask import Blueprint, request, jsonify

sort_points = Blueprint('sort_points', __name__)

@sort_points.route('/sort-points', methods=['POST'])
def sort_points_route():
    try:
        points = request.json.get('points', [])
        sorted_points = sorted(points, key=lambda x: len(x))
        return jsonify({"status": "success", "sorted_points": sorted_points})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
