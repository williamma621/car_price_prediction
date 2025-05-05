document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (result.error) {
        document.getElementById('result').innerHTML = `
            <div class="error">Error: ${result.error}</div>
        `;
    } else {
        document.getElementById('result').innerHTML = `
            <div class="success">Predicted Price: ${result.prediction}</div>
        `;
    }
});