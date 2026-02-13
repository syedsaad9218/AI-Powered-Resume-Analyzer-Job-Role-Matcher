import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "job_roles.csv")
MODEL_DIR = os.path.join(BASE_DIR, "src", "models")

os.makedirs(MODEL_DIR, exist_ok=True)
print(f"Created model directory: {MODEL_DIR}")

print(f"Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

if "Resume" not in df.columns or "Category" not in df.columns:
    raise ValueError("CSV must contain 'Resume' and 'Category' columns.")

df["Resume"] = df["Resume"].fillna("")
df["Category"] = df["Category"].fillna("Unknown")

X = df["Resume"]
y = df["Category"]

lb = LabelEncoder()
y_encoded = lb.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print("Training LinearSVC model with TF-IDF features...")
text_clf = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=15000, ngram_range=(1, 2))),
    ("clf", LinearSVC(class_weight="balanced", random_state=42)),
])
text_clf.fit(X_train, y_train)
print("Model training complete.")

y_pred = text_clf.predict(X_test)
y_test_labels = lb.inverse_transform(y_test)
y_pred_labels = lb.inverse_transform(y_pred)

print("\n--- LinearSVC Results ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
unique_labels = sorted(list(set(y_test_labels) | set(y_pred_labels)))
print(classification_report(y_test_labels, y_pred_labels, labels=unique_labels, zero_division=0))

joblib.dump(text_clf.named_steps["clf"], os.path.join(MODEL_DIR, "rf_model.pkl"))
joblib.dump(text_clf.named_steps["tfidf"], os.path.join(MODEL_DIR, "vectorizer.pkl"))
joblib.dump(lb, os.path.join(MODEL_DIR, "label_encoder.pkl"))

print("✅ Artifacts saved to app/models/")
