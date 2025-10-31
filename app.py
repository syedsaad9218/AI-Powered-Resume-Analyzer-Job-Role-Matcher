import os
import joblib
from flask import Flask, request, jsonify, render_template, send_from_directory
from upload import save_resume
from text_extract import extract_text_from_pdf
from catboost import CatBoostClassifier # <-- Import CatBoostClassifier

# --- Model & Vectorizer Loading ---
# Load the trained model and vectorizer when the app starts.
# This is much more efficient than loading them on every request.
MODEL_PATH = 'models/resume_model.cbm' # <-- Updated path
VECTORIZER_PATH = 'models/vectorizer.pkl' # <-- Updated path

model = None
vectorizer = None

try:
    # Load CatBoost model using its native method
    model = CatBoostClassifier() # <-- Initialize class
    model.load_model(MODEL_PATH) # <-- Use load_model
    
    # Load the joblib-dumped vectorizer
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ Model and vectorizer loaded successfully.")
except Exception as e: # Catching a broader exception as file/format errors can vary
    print(f"❌ Error: Model or vectorizer not found or failed to load: {e}")
    print(f"Please run 'python train_model.py' first to create the model files.")
    exit() # Stop the app if models aren't loaded

# --- Flask App Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create the uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page from the 'templates' folder."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Handles file upload, saves the file, extracts text,
    and returns a prediction.
    """
    
    # Check if the request contains the file part
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400
    
    file = request.files['resume']
    
    # Call the function from upload.py to handle the saving
    success, message_or_filename = save_resume(file, app.config['UPLOAD_FOLDER'])
    
    if not success:
        # File saving failed (e.g., wrong file type)
        return jsonify({'error': message_or_filename}), 400

    # --- Prediction Logic ---
    try:
        filename = message_or_filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 1. Extract text from the saved file
        resume_text = extract_text_from_pdf(file_path)
        
        if not resume_text.strip():
            return jsonify({'error': f'Could not extract text from {filename}. File might be empty or corrupted.'}), 400

        # 2. Transform the text using the loaded vectorizer
        # Note: vectorizer.transform() expects an iterable (like a list)
        text_vector = vectorizer.transform([resume_text])

        # 3. Predict using the loaded model
        prediction = model.predict(text_vector)
        
        # The prediction is usually an array, e.g., [['Network Security Engineer']]
        # We extract the first item.
        category = prediction[0]
        if isinstance(category, list): # Handle nested list output from some models
            category = category[0]

        # 4. Return the success message AND the prediction
        return jsonify({
            'message': f'"{filename}" uploaded successfully!',
            'category': str(category) # Convert to string for JSON
        }), 200

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': f'An error occurred during analysis: {e}'}), 500

# --- Main execution block ---
if __name__ == '__main__':
    # Note: debug=True is for development. Turn off in production.
    app.run(debug=True)