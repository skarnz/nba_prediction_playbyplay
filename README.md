# NBA Play Prediction Demo

A demonstration of an AI-powered NBA play-by-play prediction system using Azure OpenAI.

## Project Overview
This project demonstrates a web-based interface for predicting NBA plays. It uses a fine-tuned GPT-4o mini model on Azure OpenAI to analyze sequences of basketball plays and predict what will happen next.

## Features
- Input NBA play-by-play sequences
- Get AI-generated predictions for the next play
- Receive analysis of why the prediction makes sense
- Simple, intuitive web interface
- Example NBA sequences to try

## Directory Structure
- `app.py` - Flask application serving the web interface and API
- `static/` - Frontend assets
  - `css/` - Styling for the web interface
  - `js/` - JavaScript for user interactions
- `templates/` - HTML templates
- `.env` - Environment variables for API keys
- `data/` - NBA play-by-play datasets
  - `azure/` - Azure-ready datasets
    - `split/` - Split datasets for easier handling
    - `split_exp/` - Experimental datasets with additional system prompts

## Datasets
The project includes several NBA play-by-play datasets:

### Data Source
The original data comes from the following Kaggle dataset:
- **Dataset**: [NBA Play-by-Play Data 2018-2019](https://www.kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019)
- **Creator**: schmadam97
- **Contents**: Detailed play-by-play data for NBA games from multiple seasons (2015-2021)
- **Primary File**: NBA_PBP_2018-19.csv

This raw data was preprocessed to create context-target pairs for the prediction model, where each input is a sequence of plays and the target is the next play in the sequence.

### Main Datasets
- `nba_sample.jsonl` - Sample dataset with NBA play sequences (115KB)
- `nba_val.jsonl` - Validation dataset (278KB)
- `nba_train.jsonl` - Training dataset (2.1MB)

### Split Datasets
For easier handling, the main datasets have been split into smaller files:
- `nba_sample_part1of4.jsonl` to `nba_sample_part4of4.jsonl` (~29KB each)
- `nba_val_part1of4.jsonl` to `nba_val_part4of4.jsonl` (~70KB each)
- `nba_train_part1of4.jsonl` to `nba_train_part4of4.jsonl` (~557KB each)

### Experimental Datasets
These datasets include enhanced system prompts for better performance:
- `nba_sample_part1of4_exp.jsonl` to `nba_sample_part4of4_exp.jsonl`
- `nba_val_part1of4_exp.jsonl` to `nba_val_part4of4_exp.jsonl`
- `nba_train_part1of4_exp.jsonl` to `nba_train_part4of4_exp.jsonl`

## Setup Instructions

### Local Setup
1. Clone the repository
2. Install Python dependencies:
   ```
   pip install flask requests python-dotenv
   ```
3. Configure your Azure OpenAI credentials in the `.env` file:
   ```
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_DEPLOYMENT_ID=your_deployment_id
   AZURE_OPENAI_API_VERSION=your_api_version
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and visit: `http://localhost:5001`

### Google Colab Setup
1. Upload the project files to Google Drive
2. Create a new Colab notebook
3. Mount your Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
4. Navigate to the project directory:
   ```python
   %cd /content/drive/MyDrive/path/to/project
   ```
5. Install dependencies:
   ```python
   !pip install flask requests python-dotenv
   ```
6. Create a `.env` file with your Azure OpenAI credentials:
   ```python
   %%writefile .env
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_DEPLOYMENT_ID=your_deployment_id
   AZURE_OPENAI_API_VERSION=your_api_version
   ```
7. Run the application with port forwarding:
   ```python
   from google.colab.output import eval_js
   print(eval_js('google.colab.kernel.proxyPort(5001)'))
   !python app.py
   ```
8. Click the URL provided to access the application

## API Usage
The application provides a simple API endpoint:
- `POST /predict` - Sends a play sequence to get predictions
  ```json
  {
    "play_sequence": "Your NBA play-by-play sequence here"
  }
  ```

## Project Components
- **Frontend**: HTML, CSS, JavaScript for user interface
- **Backend**: Flask server handling API requests
- **AI Model**: Azure OpenAI GPT-4o mini fine-tuned on NBA data

## Requirements
- Python 3.6+
- Flask
- Requests
- python-dotenv
- Azure OpenAI API access 