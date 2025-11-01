import os
import joblib
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Import helper functions from your other files
# We assume upload.py and text_extract.py are in the same directory
try:
    from upload import save_resume
    from text_extract import extract_text_from_pdf
except ImportError:
    print("Error: Could not import 'upload.py' or 'text_extract.py'.")
    print("Please make sure these files are in the same directory as app.py.")
    exit()

# --- 1. App Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB file size limit

# --- 2. Load Model Artifacts ---
MODEL_PATH = 'models/rf_model.pkl'
VECTORIZER_PATH = 'models/vectorizer.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

model = None
vectorizer = None
label_encoder = None

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    print("✅ Model, vectorizer, and label encoder loaded successfully.")
except FileNotFoundError:
    print(f"❌ Error: Model or artifact files not found.")
    print(f"Please run 'python train_model.py' first to create the model files in the 'models/' directory.")
    exit()
except Exception as e:
    print(f"❌ Error loading models: {e}")
    exit()

# Create the uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- 3. Define Routes ---

@app.route('/')
def index():
    """Renders the main HTML page."""
    # Flask will look for 'index.html' in a folder named 'templates'
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_category():
    """Handles the file upload, text extraction, and prediction."""
    
    # Check if a file is in the request
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400
    
    file = request.files['resume']

    # --- 1. Save the file ---
    # Use the helper function from upload.py
    try:
        success, message_or_filename = save_resume(file, app.config['UPLOAD_FOLDER'])
        
        if not success:
            return jsonify({'error': message_or_filename}), 400
        
        filename = message_or_filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    except Exception as e:
        return jsonify({'error': f'Error saving file: {str(e)}'}), 500

    # --- 2. Extract text ---
    try:
        resume_text = extract_text_from_pdf(file_path)
        
        if not resume_text or not resume_text.strip():
            return jsonify({'error': f'Could not extract text from {filename}. File might be empty or corrupted.'}), 400

    except Exception as e:
        return jsonify({'error': f'Error extracting text: {str(e)}'}), 500

    # --- 3. Predict category ---
    try:
        # Transform the text using the loaded vectorizer
        text_vector = vectorizer.transform([resume_text])

        # Predict the numeric category
        prediction_numeric = model.predict(text_vector)
        
        # Convert the numeric category back to a string label
        # prediction_numeric[0] gets the first (and only) prediction
        category_label = label_encoder.inverse_transform(prediction_numeric)[0]

        # 4. Return the result
        return jsonify({
            'message': f'\"{filename}\" analyzed successfully!',
            'category': str(category_label)  # Send the string label
        }), 200

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': f'An error occurred during analysis: {str(e)}'}), 500

# --- 4. Run the App ---
if __name__ == '__main__':
    # Set debug=True for development (shows errors in browser)
    # Set debug=False for production
    app.run(debug=True)
