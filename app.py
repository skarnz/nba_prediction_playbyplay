"""
NBA Play Prediction Demo

A simple Flask application that provides an interface to demonstrate 
the fine-tuned GPT-4o mini model for NBA play prediction.
"""

import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API configuration from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT_ID = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Set up Flask application
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    """Render the main prediction interface."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests by calling the Azure OpenAI API
    with the user-provided play sequence.
    """
    # Get play sequence from request
    data = request.json
    play_sequence = data.get('play_sequence', '')
    
    if not play_sequence.strip():
        return jsonify({
            'error': 'Please enter a play sequence'
        }), 400
    
    # Prepare the API request
    system_message = "You are a sports play prediction assistant that predicts the next play in NBA games based on previous plays, considering the score, time remaining, and recent player activity. Provide accurate and detailed predictions in the format: Q1 3:39 | TEAM | PLAYER ACTION | SCORE"
    
    prompt = f"Based on the following NBA play-by-play sequence, predict what will happen next:\n\n{play_sequence}"
    
    # Construct API URL
    api_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_ID}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
    
    # Prepare headers and payload
    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_OPENAI_API_KEY
    }
    
    payload = {
        'messages': [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        'temperature': 0.2,
        'max_tokens': 50
    }
    
    try:
        # Make the API request
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        # Parse the response
        result = response.json()
        prediction = result['choices'][0]['message']['content'].strip()
        
        # Get analysis of the prediction
        analysis = get_prediction_analysis(play_sequence, prediction)
        
        return jsonify({
            'prediction': prediction,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({
            'error': f"Error making prediction: {str(e)}"
        }), 500

def get_prediction_analysis(play_sequence, prediction):
    """
    Get an analysis of why the prediction makes sense given the play sequence.
    """
    system_message = "You are a sports analyst who explains NBA play predictions. Explain why the predicted play makes sense given the previous sequence."
    
    prompt = f"""
    Previous play sequence:
    {play_sequence}
    
    Predicted next play:
    {prediction}
    
    Explain why this prediction makes sense based on player positioning, game situation, score, and typical patterns.
    """
    
    # Construct API URL - use the same model for analysis
    api_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_ID}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
    
    # Prepare headers and payload
    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_OPENAI_API_KEY
    }
    
    payload = {
        'messages': [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        'temperature': 0.7,
        'max_tokens': 200
    }
    
    try:
        # Make the API request
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        analysis = result['choices'][0]['message']['content'].strip()
        
        return analysis
    
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

# Define example play sequences for the demo
@app.route('/examples', methods=['GET'])
def get_examples():
    examples = [
        "Q1 5:33 | IND | Offensive rebound by M. Turner | MEM 8, IND 10\nQ1 5:32 | IND | M. Turner misses 2-pt layup from 1 ft | MEM 8, IND 10\nQ1 5:31 | IND | Offensive rebound by M. Turner | MEM 8, IND 10\nQ1 5:31 | IND | M. Turner makes 2-pt layup from 1 ft | MEM 8, IND 12\nQ1 5:18 | MEM | M. Conley misses 2-pt layup from 5 ft | MEM 8, IND 12\nQ1 5:14 | IND | Defensive rebound by B. Bogdanovi | MEM 8, IND 12\nQ1 5:12 | IND | Personal foul by C. Parsons (drawn by B. Bogdanovi) | MEM 8, IND 12\nQ1 5:12 | MEM | K. Anderson enters the game for J. Green | MEM 8, IND 12\nQ1 5:12 | MEM | J. Jackson enters the game for C. Parsons | MEM 8, IND 12\nQ1 4:58 | IND | Turnover by D. Collison (lost ball; steal by J. Jackson) | MEM 8, IND 12",
        
        "Q3 4:51 | BRK | Violation by Team (delay of game) | BRK 63, DET 76\nQ3 4:51 | BRK | Violation by Team (kicked ball) | BRK 63, DET 76\nQ3 4:49 | DET | Personal foul by T. Graham (drawn by B. Griffin) | BRK 63, DET 76\nQ3 4:36 | DET | R. Jackson misses 3-pt jump shot from 29 ft | BRK 63, DET 76\nQ3 4:30 | BRK | Defensive rebound by C. LeVert | BRK 63, DET 76\nQ3 4:27 | BRK | C. LeVert makes 2-pt layup from 3 ft | BRK 65, DET 76\nQ3 4:21 | DET | L. Galloway misses 3-pt jump shot from 27 ft | BRK 65, DET 76\nQ3 4:21 | BRK | Defensive rebound by S. Dinwiddie | BRK 65, DET 76\nQ3 4:15 | BRK | C. LeVert misses 3-pt jump shot from 26 ft | BRK 65, DET 76\nQ3 4:12 | DET | Defensive rebound by Z. Pachulia | BRK 65, DET 76"
    ]
    
    return jsonify(examples)

if __name__ == '__main__':
    # Check if environment variables are set
    if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, 
                AZURE_OPENAI_DEPLOYMENT_ID, AZURE_OPENAI_API_VERSION]):
        print("Error: Required environment variables are not set. Please check your .env file.")
        exit(1)
    
    print("Starting NBA Play Prediction Demo...")
    app.run(debug=True, host='0.0.0.0', port=5001) 