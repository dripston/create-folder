import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def create_user_folder(user_id):
    """
    Creates a folder for the given user ID with required files if it doesn't exist.
    
    Args:
        user_id (str): The user identifier
    """
    # Check if folder already exists
    if os.path.exists(user_id):
        return read_user_data(user_id)
    
    # Create the user folder
    os.makedirs(user_id)
    
    # Define the file paths
    memory_file = os.path.join(user_id, "memory.json")
    logs_file = os.path.join(user_id, "logs.json")
    index_file = os.path.join(user_id, "index.html")
    schedule_file = os.path.join(user_id, "schedule.json")
    
    # Create empty JSON files
    with open(memory_file, 'w') as f:
        json.dump({}, f)
    
    with open(logs_file, 'w') as f:
        json.dump([], f)
    
    with open(schedule_file, 'w') as f:
        json.dump({}, f)
    
    # Create a basic HTML file
    with open(index_file, 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>User Page</title>\n</head>\n<body>\n<h1>Welcome User</h1>\n</body>\n</html>")
    
    return read_user_data(user_id)

def read_user_data(user_id):
    """
    Reads and returns the data from all files in the user folder.
    
    Args:
        user_id (str): The user identifier
        
    Returns:
        dict: Dictionary containing data from all files
    """
    if not os.path.exists(user_id):
        return None
    
    user_data = {}
    
    # Read memory.json
    memory_file = os.path.join(user_id, "memory.json")
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            user_data["memory"] = json.load(f)
    
    # Read logs.json
    logs_file = os.path.join(user_id, "logs.json")
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            user_data["logs"] = json.load(f)
    
    # Read schedule.json
    schedule_file = os.path.join(user_id, "schedule.json")
    if os.path.exists(schedule_file):
        with open(schedule_file, 'r') as f:
            user_data["schedule"] = json.load(f)
    
    # Read index.html
    index_file = os.path.join(user_id, "index.html")
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            user_data["index"] = f.read()
    
    return user_data

def update_user_file(user_id, file_name, data):
    """
    Updates a specific file for a user with new data.
    
    Args:
        user_id (str): The user identifier
        file_name (str): Name of the file to update
        data (any): New data to write to the file
        
    Returns:
        dict: Updated user data or error message
    """
    # Check if user folder exists
    if not os.path.exists(user_id):
        return {"error": f"User folder '{user_id}' does not exist."}
    
    # Validate file name
    valid_files = ["memory.json", "logs.json", "schedule.json", "index.html"]
    if file_name not in valid_files:
        return {"error": f"Invalid file name. Valid files: {valid_files}"}
    
    file_path = os.path.join(user_id, file_name)
    
    try:
        if file_name.endswith(".json"):
            # Write JSON data
            with open(file_path, 'w') as f:
                json.dump(data, f)
        else:
            # Write HTML or other text data
            with open(file_path, 'w') as f:
                f.write(data)
        
        # Return updated user data
        return read_user_data(user_id)
    except Exception as e:
        return {"error": f"Failed to update file: {str(e)}"}

@app.route('/')
def home():
    return jsonify({
        "message": "User Folder Creation and Update Service",
        "endpoints": {
            "create_user": "/create-user/<user_id>",
            "get_user_data": "/user/<user_id>",
            "update_user_file": "/user/<user_id>/<file_name>"
        }
    })

@app.route('/create-user/<user_id>')
def create_user_endpoint(user_id):
    try:
        user_data = create_user_folder(user_id)
        return jsonify({
            "user_id": user_id,
            "data": user_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/<user_id>')
def get_user_data(user_id):
    try:
        user_data = read_user_data(user_id)
        if user_data is None:
            return jsonify({"error": f"User folder '{user_id}' does not exist."}), 404
        return jsonify({
            "user_id": user_id,
            "data": user_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/<user_id>/<file_name>', methods=['PUT'])
def update_user_file_endpoint(user_id, file_name):
    try:
        # Get data from request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must contain JSON data."}), 400
        
        # Extract the actual data to update
        update_data = data.get("data")
        if update_data is None:
            return jsonify({"error": "Request body must contain 'data' field."}), 400
        
        result = update_user_file(user_id, file_name, update_data)
        
        if "error" in result:
            return jsonify(result), 400
            
        return jsonify({
            "user_id": user_id,
            "file": file_name,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))