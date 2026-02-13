// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    
    // Get references to the DOM elements
    const form = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');
    const predictionDiv = document.getElementById('prediction-result');
    const fileInput = document.getElementById('resume-file');

    // Add a 'submit' event listener to the form
    form.addEventListener('submit', (event) => {
        // Prevent the default form submission (which reloads the page)
        event.preventDefault();

        // Show a loading message and clear old results
        resultDiv.textContent = 'Uploading and analyzing...';
        resultDiv.style.color = '#a5b4fc'; // Light indigo color
        predictionDiv.textContent = ''; // Clear previous prediction

        // Get the form data
        const formData = new FormData(form);
        const resumeFile = fileInput.files[0];

        // Basic client-side validation
        if (!resumeFile) {
            resultDiv.textContent = 'Please select a file to upload.';
            resultDiv.style.color = '#f87171'; // Red color
            return;
        }
        
        // Disable button to prevent multiple submissions
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Analyzing...';
        submitButton.classList.add('opacity-50', 'cursor-not-allowed');

        // Use the fetch API to send the file to your Flask server
        fetch('/predict', {
            method: 'POST',
            body: formData, // Send the form data (which includes the file)
        })
        .then(response => {
            // Check if the response is successful, if not, parse it as text
            if (!response.ok) {
                 // Try to parse error as JSON, fallback to plain text
                return response.json().then(errData => {
                    throw new Error(errData.error || 'Unknown server error');
                }).catch(() => {
                    throw new Error(`Server responded with status: ${response.status}`);
                });
            }
            return response.json(); // Get the JSON response from the server
        })
        .then(data => {
            // Handle success
            if (data.message) {
                resultDiv.textContent = data.message;
                resultDiv.style.color = '#6ee7b7'; // Green color
            }
            
            // Display the prediction
            if (data.category) {
                predictionDiv.textContent = `${data.category}`;
            }
        })
        .catch(error => {
            // Handle errors (from network or server)
            console.error('Error:', error);
            resultDiv.textContent = `Error: ${error.message}`;
            resultDiv.style.color = '#f87171'; // Red color
            predictionDiv.textContent = ''; // Clear prediction text on error
        })
        .finally(() => {
            // Re-enable the button regardless of success or failure
            submitButton.disabled = false;
            submitButton.textContent = 'Predict Category';
            submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
            
            // Clear the file input for the next upload
            // Note: This might not be desirable for all users, but it's clean
            // fileInput.value = ''; 
        });
    });
});
