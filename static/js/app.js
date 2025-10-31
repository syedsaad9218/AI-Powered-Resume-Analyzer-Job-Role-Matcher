document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');
    const predictionDiv = document.getElementById('prediction-result');
    const fileInput = document.getElementById('resume-file');

    form.addEventListener('submit', (event) => {
        // Prevent the default form submission (which reloads the page)
        event.preventDefault();

        // Show a loading message and clear old results
        resultDiv.textContent = 'Uploading and analyzing...';
        resultDiv.style.color = '#a5b4fc'; // Light indigo color
        predictionDiv.textContent = ''; // Clear previous prediction

        // Create a FormData object from the form
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
        fetch('/analyze', {
            method: 'POST',
            body: formData, // The FormData object contains the file
        })
        .then(response => response.json()) // Get the JSON response from the server
        .then(data => {
            // Display the server's message
            if (data.message) {
                resultDiv.textContent = data.message;
                resultDiv.style.color = '#6ee7b7'; // Green color
            }
            
            // Display the prediction
            if (data.category) {
                predictionDiv.textContent = `Predicted Category: ${data.category}`;
            }

            // Handle errors from the server
            if (data.error) {
                resultDiv.textContent = `Error: ${data.error}`;
                resultDiv.style.color = '#f87171'; // Red color
                predictionDiv.textContent = ''; // Clear prediction text on error
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Error:', error);
            resultDiv.textContent = 'An unexpected network error occurred. Please try again.';
            resultDiv.style.color = '#f87171'; // Red color
        })
        .finally(() => {
            // Re-enable the button regardless of success or failure
            submitButton.disabled = false;
            submitButton.textContent = 'Predict Category';
            submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
            
            // Clear the file input for the next upload
            fileInput.value = '';
        });
    });
});
