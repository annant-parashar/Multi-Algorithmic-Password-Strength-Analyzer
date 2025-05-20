document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('passwordInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const generateBtn = document.getElementById('generateBtn');
    const resultContainer = document.getElementById('resultContainer');
    const strengthMeter = document.getElementById('strengthMeter');
    const strengthText = document.getElementById('strengthText');
    const lengthScore = document.getElementById('lengthScore');
    const complexityScore = document.getElementById('complexityScore');
    const dictionaryScore = document.getElementById('dictionaryScore');
    const bruteforceScore = document.getElementById('bruteforceScore');
    const suggestionsList = document.getElementById('suggestionsList');

    analyzeBtn.addEventListener('click', async () => {
        const password = passwordInput.value;
        if (!password) {
            alert('Please enter a password');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password }),
            });

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to analyze password. Please try again.');
        }
    });

    generateBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('http://localhost:5000/generate');
            const result = await response.json();
            passwordInput.value = result.password;
            analyzeBtn.click();
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate password. Please try again.');
        }
    });

    function displayResults(result) {
        resultContainer.style.display = 'block';

        // Update scores
        updateScore(strengthMeter, result.total_score);
        updateScore(lengthScore, result.length_score);
        updateScore(complexityScore, result.complexity_score);
        updateScore(dictionaryScore, result.dictionary_score);
        updateScore(bruteforceScore, result.bruteforce_score);

        // Update strength text and color
        const strengthClass = getStrengthClass(result.total_score);
        strengthMeter.className = `meter-fill ${strengthClass}`;
        strengthText.textContent = getStrengthText(result.total_score);

        // Update suggestions
        suggestionsList.innerHTML = result.suggestions
            .map(suggestion => `<li>${suggestion}</li>`)
            .join('');
    }

    function updateScore(element, score) {
        element.style.width = `${score * 100}%`;
    }

    function getStrengthClass(score) {
        if (score < 0.4) return 'weak';
        if (score < 0.7) return 'moderate';
        return 'strong';
    }

    function getStrengthText(score) {
        if (score < 0.4) return 'Weak';
        if (score < 0.7) return 'Moderate';
        return 'Strong';
    }
});
