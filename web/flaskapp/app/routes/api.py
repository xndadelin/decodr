from flask import Blueprint, request, jsonify
import sys
import os

from pydecodr.api import ENCODING_MAP, encode, decode, encrypt, decrypt, crack, detect

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/operations', methods=['GET'])
def list_operations():
    from app.utils.operation_metadata import get_operations_metadata
    return jsonify(get_operations_metadata())

@bp.route('/execute', methods=["POST"])
def execute_operation():
    data = request.json

    if not data:
        return jsonify({
            "success": False,
            "error": "Ooops! No data provided!"
        }), 400
    
    operation = data.get('operation')
    action = data.get('action')
    input_text = data.get('input', '')
    params = data.get('params', {})

    if not operation or not action:
        return jsonify({
            "success": False,
            "error": "Opps! Missing operation or action"
        }), 400
    
    try: 
        action_map = {
            'encode': encode,
            'decode': decode,
            "encrypt": encrypt,
            "decrypt": decrypt,
            "crack": crack
        }

        if action not in action_map:
            return jsonify({
                "succcess": False,
                "error": f"Invalid action: {action}"
            }), 400
        
        func = action_map[action]
        result = func(operation, input_text, **params)

        return jsonify({
            "success": True,
            "output": result,
            "operation": operation,
            "action": action
        })
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"Unsupported operation: {str(e)}"
        }), 400
    except AttributeError as e:
        return jsonify({
            "success": False,
            "error": f"Attribute error: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Execution error: {str(e)}"
        }), 500