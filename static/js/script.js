document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const playInput = document.getElementById('play-input');
    const predictButton = document.getElementById('predict-button');
    const clearButton = document.getElementById('clear-button');
    const exampleButton = document.getElementById('example-button');
    const resultsSection = document.getElementById('results-section');
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error-message');
    const predictionResultsElement = document.getElementById('prediction-results');
    
    // Example NBA play sequences
    const examples = [
        "Q1 11:45 - Jump Ball: MIL wins the jump ball\nQ1 11:45 - MIL gains possession\nQ1 11:38 - Lopez 25' 3PT Jump Shot (MIL 3-0)\nQ1 11:38 - Antetokounmpo Assist (MIL 3-0)\nQ1 11:23 - MISS Irving Step Back Jump Shot\nQ1 11:20 - Lopez Defensive Rebound\nQ1 11:13 - MISS Antetokounmpo Cutting Layup Shot\nQ1 11:13 - Antetokounmpo Offensive Rebound\nQ1 11:10 - MISS Antetokounmpo Tip Layup Shot\nQ1 11:10 - Durant Defensive Rebound",
        
        "Q2 5:45 - Tatum driving layup (BOS 48-47)\nQ2 5:30 - MISS Butler 14' fadeaway\nQ2 5:28 - Robert Williams defensive rebound\nQ2 5:20 - Brown 26' 3PT running pull-up (BOS 51-47)\nQ2 5:05 - Adebayo 12' pullup jump shot (BOS 51-49)\nQ2 4:45 - Tatum 12' floating jump shot (BOS 53-49)\nQ2 4:28 - MISS Vincent 30' 3PT pullup jump shot\nQ2 4:26 - Brown defensive rebound",
        
        "Q4 2:10 - MISS Curry 29' 3PT\nQ4 2:07 - Thompson offensive rebound\nQ4 2:05 - Thompson 21' jumper (GSW 103-97)\nQ4 1:42 - Green shooting foul\nQ4 1:42 - Tatum free throw 1 of 2 (GSW 103-98)\nQ4 1:42 - Tatum free throw 2 of 2 (GSW 103-99)\nQ4 1:31 - MISS Thompson 28' 3PT\nQ4 1:28 - Horford defensive rebound\nQ4 1:19 - MISS Brown 25' 3PT"
    ];
    
    // Event listeners
    predictButton.addEventListener('click', predictNextPlay);
    clearButton.addEventListener('click', clearInput);
    exampleButton.addEventListener('click', loadExample);
    
    // Load a random example
    function loadExample() {
        const randomExample = examples[Math.floor(Math.random() * examples.length)];
        playInput.value = randomExample;
    }
    
    // Clear input and results
    function clearInput() {
        playInput.value = '';
        resultsSection.classList.remove('active');
        errorElement.classList.remove('active');
    }
    
    // Predict next play
    async function predictNextPlay() {
        const playSequence = playInput.value.trim();
        
        if (!playSequence) {
            showError('Please enter a play sequence');
            return;
        }
        
        // Show loading and hide any previous results/errors
        resultsSection.classList.add('active');
        loadingElement.classList.add('active');
        errorElement.classList.remove('active');
        predictionResultsElement.innerHTML = '';
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ play_sequence: playSequence })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to get prediction');
            }
            
            // Hide loading
            loadingElement.classList.remove('active');
            
            // Display prediction
            displayPrediction(data);
            
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'Something went wrong. Please try again.');
            loadingElement.classList.remove('active');
        }
    }
    
    // Display prediction
    function displayPrediction(data) {
        const { prediction, analysis } = data;
        
        const resultHtml = `
            <div class="prediction-card">
                <h3>Predicted Next Play</h3>
                <p>${prediction}</p>
            </div>
            
            <div class="prediction-card">
                <h3>Analysis</h3>
                <p>${analysis}</p>
            </div>
            
            <div class="accordion">
                <div class="accordion-header" onclick="toggleAccordion(this)">
                    <h3>Why This Prediction?</h3>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-content">
                    <p>This prediction is based on patterns observed in the sequence of plays you provided, taking into account game context, player positions, and team momentum.</p>
                </div>
            </div>
        `;
        
        predictionResultsElement.innerHTML = resultHtml;
    }
    
    // Show error message
    function showError(message) {
        errorElement.textContent = message;
        errorElement.classList.add('active');
    }
});

// Toggle accordion
function toggleAccordion(element) {
    const content = element.nextElementSibling;
    content.classList.toggle('active');
    
    const icon = element.querySelector('.accordion-icon');
    icon.classList.toggle('active');
} 