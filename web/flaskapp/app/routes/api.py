"""
{
    "input": "SGVsbG8=",
    "recipe": [
        {"operation": "base64", "action": "decode"},
        {"operation": "caesar", "action": "decrypt", "params": {"shift": 3}}
    ]
}

{
    "operation": "caesar",
    "action": "decrypt",
    "input": "KHOOR",
    "params": {"shift": 3}
}

"""

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
    
@bp.route('/execute-recipe', methods=['POST'])
def execute_recipe():
    data = request.json

    if not data:
        return jsonify({
            "success": False,
            "error": "Oops! No data provided!"
        }), 400
    
    input_text = data.get('input', '')
    recipe = data.get('recipe', [])

    if not recipe:
        return jsonify({
            "success": False,
            "error": "Empty recipe, oops!"
        }), 400
    
    result = input_text
    steps = []
    
    action_map = {
        'encode': encode,
        'decode': decode,
        "encrypt": encrypt,
        "decrypt": decrypt,
        "crack": crack
    }

    for i, step in enumerate(recipe):
        operation = step.get('operation')
        action = step.get('action')
        params = step.get('params', {})   

        try:
            if action not in action_map:
                raise ValueError(f"Invalid action: {action}")
            
            func = action_map[action]
            result = func(operation, result, **params)

            steps.append({
                "step": i + 1,
                'operation': operation,
                "action": action,
                "output": result,
                "success": True
            })
        except Exception as e:
            steps.append({
                "step": i + 1,
                'operation': operation,
                "action": action,
                "error": str(e),
                "success": False
            })
            return jsonify({
                "success": False,
                "output": result, 
                "steps": steps,
                "error": f"Failed at step {i + 1}: {str(e)}"
            }), 400
        
    return jsonify({
        'success': True,
        "output": result,
        "steps": steps
    })