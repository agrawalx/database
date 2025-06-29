# app.py
from flask import Flask, request, jsonify
import pandas as pd
import os

# Initialize the Flask application
app = Flask(__name__)

# --- Database Loading ---
# Construct the full path to the CSV file.
data_path = os.path.join(os.path.dirname(__file__), 'mock_database.csv')

try:
    # Load the mock database from the CSV file
    db = pd.read_csv(data_path)
    # Ensure the 'YOB' column is treated as a string for consistent matching
    db['YOB'] = db['YOB'].astype(str)
except FileNotFoundError:
    # Create an empty DataFrame if the file doesn't exist
    db = pd.DataFrame(columns=['Name', 'YOB'])
    print("WARNING: mock_database.csv not found. Running with an empty database.")


# --- API Endpoint ---
@app.route('/verify', methods=['GET'])
def verify_identity():
    """
    Verifies if a user's name and year of birth (YOB) exist in the database.
    Expects 'name' and 'yob' as query parameters.
    
    Example usage:
    /verify?name=Alice&yob=1990
    """
    # Get 'name' and 'yob' from the request's query parameters
    user_name = request.args.get('name')
    user_yob = request.args.get('yob')

    # --- Input Validation ---
    if not user_name or not user_yob:
        return jsonify({"error": "Missing required parameters: 'name' and 'yob'"}), 400

    # --- Database Query ---
    try:
        # Search for a matching record (case-insensitive for name)
        match = db[(db['Name'].str.lower() == user_name.lower()) & (db['YOB'] == user_yob)]

        # --- Response Logic ---
        if not match.empty:
            # Match found: return result: 1 (True)
            return jsonify({"result": 1})
        else:
            # No match found: return result: 0 (False)
            return jsonify({"result": 0})
            
    except Exception as e:
        # --- Error Handling ---
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

# This allows the script to be run directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
