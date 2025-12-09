import os
import json
import sys

def create_user_folder(user_id):
    """
    Creates a folder for the given user ID with required files if it doesn't exist.
    
    Args:
        user_id (str): The user identifier
    """
    # Check if folder already exists
    if os.path.exists(user_id):
        print(f"Folder '{user_id}' already exists. No action taken.")
        return read_user_data(user_id)
    
    # Create the user folder
    os.makedirs(user_id)
    print(f"Created folder '{user_id}'")
    
    # Define the file paths
    memory_file = os.path.join(user_id, "memory.json")
    logs_file = os.path.join(user_id, "logs.json")
    index_file = os.path.join(user_id, "index.html")
    schedule_file = os.path.join(user_id, "schedule.json")
    
    # Create empty JSON files
    with open(memory_file, 'w') as f:
        json.dump({}, f)
    print(f"Created {memory_file}")
    
    with open(logs_file, 'w') as f:
        json.dump([], f)
    print(f"Created {logs_file}")
    
    with open(schedule_file, 'w') as f:
        json.dump({}, f)
    print(f"Created {schedule_file}")
    
    # Create a basic HTML file
    with open(index_file, 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>User Page</title>\n</head>\n<body>\n<h1>Welcome User</h1>\n</body>\n</html>")
    print(f"Created {index_file}")
    
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
        print(f"Folder '{user_id}' does not exist.")
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_user_folder.py <user_id>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    user_data = create_user_folder(user_id)
    
    if user_data:
        print("\n--- User Data ---")
        print(json.dumps(user_data, indent=2))