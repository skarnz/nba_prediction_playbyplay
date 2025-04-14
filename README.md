# NBA Play Prediction Demo

A demonstration of an AI-powered NBA play-by-play prediction system using Azure OpenAI.

## Project Overview
This project demonstrates a web-based interface for predicting NBA plays. It uses a fine-tuned GPT-4o mini model on Azure OpenAI to analyze sequences of basketball plays and predict what will happen next.

## Use Case Justification
Sports play prediction represents an innovative application of transformer models beyond traditional text generation tasks. By predicting the next play in an NBA game sequence:

1. We demonstrate the model's ability to understand complex sequential patterns in specialized domains
2. The task requires understanding basketball-specific context, including team dynamics, player tendencies, game clock, and score situations
3. It serves as a proof of concept for AI assistance in sports analysis, coaching, and broadcasting

## Use Case Benefits
This application offers several potential benefits:

1. **Sports Broadcasting**: Enhancing live commentary with AI-powered predictions
2. **Coaching Tools**: Helping coaches anticipate opponent strategies in game situations
3. **Fan Engagement**: Creating interactive experiences for fans to predict and compare with AI
4. **Sports Analytics**: Providing insights into game patterns and tendencies
5. **Educational Value**: Teaching basketball strategy through AI-predicted outcomes

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

### Dataset Justification
This dataset was chosen for several compelling reasons:

1. **Comprehensive Coverage**: Contains detailed play-by-play data for entire NBA seasons, providing a rich source of sequential patterns
2. **Structured Format**: Each play has consistent formatting with quarter, time, team, action, and score information
3. **Context Richness**: Contains sufficient context (player names, actions, game situations) that enables meaningful predictions
4. **Volume**: With thousands of sequences, provides enough examples for fine-tuning a large language model
5. **Real-world Applicability**: Based on actual professional games, making predictions relevant to real basketball scenarios

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

## Model Selection

### Chosen Model: GPT-4o mini (Azure OpenAI)
For this project, we selected GPT-4o mini on Azure OpenAI for the following reasons:

1. **Contextual Understanding**: Excels at understanding complex contexts in sequential data
2. **Few-shot Learning Capability**: Can quickly adapt to new patterns with limited examples
3. **Specialized Knowledge**: Retains general knowledge about basketball, teams, and players
4. **Size Efficiency**: Smaller than full GPT-4o while maintaining strong performance on specialized tasks
5. **API Accessibility**: Azure OpenAI provides stable API access for deployment

### Model Fine-tuning Approach
The model was fine-tuned using:
- Specialized system prompts tailored to NBA play prediction
- Context-target pairs from preprocessed NBA play-by-play data
- Consistent formatting to enhance pattern recognition

## Model Comparisons
During development, several alternative models were considered:

1. **T5-base**: 
   - Pro: Specifically designed for text-to-text tasks
   - Con: Smaller parameter count limited performance on complex basketball sequences

2. **BART-large**:
   - Pro: Strong performance on sequence-to-sequence tasks
   - Con: Less domain-specific knowledge than larger models

3. **GPT-3.5 Turbo**:
   - Pro: Good general language capabilities
   - Con: Less context window than GPT-4o mini

4. **Local LLaMA models**:
   - Pro: Full local control without API dependencies
   - Con: Required more extensive fine-tuning and computational resources

GPT-4o mini was ultimately selected for its optimal balance of performance, efficiency, and deployment ease.

## Evaluation Process
To evaluate the model's performance on NBA play prediction, we implemented the following approach:

### Quantitative Metrics
- **Prediction Accuracy**: Measuring exact matches between predicted and actual next plays
- **Play Type Accuracy**: Evaluating if the model correctly predicts the general type of play (shot, pass, rebound, etc.)
- **Rouge-L Score**: Measuring the longest common subsequence between predictions and ground truth
- **Time/Position Accuracy**: Assessing the model's ability to maintain game flow context

### Qualitative Evaluation
- **Human Expert Review**: Basketball experts reviewing predictions for tactical plausibility
- **Context Coherence**: Evaluating if predictions maintain consistency with game situation and score
- **Interactive Testing**: Using the web interface to test varied input sequences and assess prediction quality

### Refinement Strategy
The fine-tuning process incorporated:
- Iterative system prompt improvements based on performance analysis
- Testing variations in temperature and top-p sampling parameters
- Sample-efficient fine-tuning focusing on high-quality examples

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

## Future Improvements
- Implement additional metrics for more comprehensive model evaluation
- Experiment with different model architectures tailored to sports sequence prediction
- Add visualization tools for analyzing prediction patterns and biases
- Develop an expanded dataset covering more seasons and leagues 