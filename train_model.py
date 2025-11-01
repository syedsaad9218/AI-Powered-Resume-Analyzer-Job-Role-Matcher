import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# --- 1. Create Directories ---
# Create a 'models' directory if it doesn't exist
os.makedirs('models', exist_ok=True)
print("Created 'models' directory.")

# --- 2. Load Data ---
print("Loading 'job_roles.csv'...")
try:
    df = pd.read_csv("job_roles.csv")
except FileNotFoundError:
    print("Error: 'job_roles.csv' not found.")
    print("Please make sure the CSV file is in the same directory as this script.")
    exit()

# Check for required columns
if "Resume" not in df.columns or "Category" not in df.columns:
    print("Error: CSV must contain 'Resume' and 'Category' columns.")
    exit()

print("Data loaded successfully.")

# --- 3. Preprocessing ---
print("Preprocessing data...")
# Handle potential missing values just in case
df['Resume'].fillna('', inplace=True)
df['Category'].fillna('Unknown', inplace=True)

# Features and Labels
X = df["Resume"]
y = df["Category"]

# Encode labels (e.g., "Python Developer" -> 0)
lb = LabelEncoder()
y_encoded = lb.fit_transform(y)

# Vectorize text
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
X_vectorized = tfidf.fit_transform(X)

print("Preprocessing complete.")

# --- 4. Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# --- 5. Train Model ---
print("Training Random Forest model...")
# We'll use the Random Forest model as it's robust
rf_model = OneVsRestClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
rf_model.fit(X_train, y_train)
print("Model training complete.")

# --- 6. Evaluate Model (Optional, but good practice) ---
y_pred_rf = rf_model.predict(X_test)
# We need to get the original labels for the report
y_test_labels = lb.inverse_transform(y_test)
y_pred_labels = lb.inverse_transform(y_pred_rf)

print('\n--- Random Forest Classifier Results ---')
print(f'Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}')
# Filter labels that are present in both test and prediction for the report
unique_labels = sorted(list(set(y_test_labels) | set(y_pred_labels)))
print(f'Classification Report:\n{classification_report(y_test_labels, y_pred_labels, labels=unique_labels, zero_division=0)}')

# --- 7. Save Artifacts ---
print("\nSaving model, vectorizer, and label encoder to 'models/' directory...")
joblib.dump(rf_model, 'models/rf_model.pkl')
joblib.dump(tfidf, 'models/vectorizer.pkl')
joblib.dump(lb, 'models/label_encoder.pkl')

print("✅ All artifacts saved successfully.")
print("You can now run the Flask app using 'python app.py' or 'flask run'.")
