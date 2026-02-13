import os
import joblib
from flask import Blueprint, request, jsonify, render_template, current_app

from .upload import save_resume
from .services.text_extract import extract_text_from_pdf

bp = Blueprint("main", __name__)

# model files are under app/models in your new structure
MODEL_PATH = os.path.join("src", "models", "rf_model.pkl")
VECTORIZER_PATH = os.path.join("src", "models", "vectorizer.pkl")
LABEL_ENCODER_PATH = os.path.join("src", "models", "label_encoder.pkl")

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    print("✅ Model, vectorizer, and label encoder loaded successfully.")
except FileNotFoundError:
    print("❌ Model files not found. Run training first: python scripts/train_model.py")
    raise
except Exception as e:
    print(f"❌ Error loading model artifacts: {e}")
    raise


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/predict", methods=["POST"])
def predict_category():
    if "resume" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["resume"]

    # 1) Save file
    try:
        success, message_or_filename = save_resume(file, current_app.config["UPLOAD_FOLDER"])
        if not success:
            return jsonify({"error": message_or_filename}), 400

        filename = message_or_filename
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    except Exception as e:
        return jsonify({"error": f"Error saving file: {str(e)}"}), 500

    # 2) Extract text
    try:
        resume_text = extract_text_from_pdf(file_path)
        if not resume_text or not resume_text.strip():
            return jsonify({"error": f"Could not extract text from {filename}. File might be empty, scanned, or corrupted."}), 400

        normalized_text = " ".join(resume_text.split())
        current_app.logger.info("Extracted %d characters from %s", len(normalized_text), filename)
        current_app.logger.debug("Extracted text preview (%s): %s", filename, normalized_text[:250])
    except Exception as e:
        return jsonify({"error": f"Error extracting text: {str(e)}"}), 500

    # 3) Predict
    try:
        text_vector = vectorizer.transform([normalized_text])
        current_app.logger.info(
            "Vectorized %s into %d features (%d non-zero)",
            filename,
            text_vector.shape[1],
            text_vector.nnz
        )

        prediction_numeric = model.predict(text_vector)
        category_label = label_encoder.inverse_transform(prediction_numeric)[0]

        return jsonify({
            "message": f"\"{filename}\" analyzed successfully!",
            "category": str(category_label)
        }), 200
    except Exception as e:
        current_app.logger.exception("Error during prediction for %s", filename)
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500
