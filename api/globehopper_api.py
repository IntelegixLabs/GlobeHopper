from flask import Blueprint, jsonify
from flask_api import status

globehopper_Blueprint = Blueprint('globehopper_Blueprint', __name__)


@globehopper_Blueprint.route('/demo', methods=['POST'])
def chat_bot():
    try:
        return jsonify({"message": f"Module - Error "}), status.HTTP_400_BAD_REQUEST
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST
