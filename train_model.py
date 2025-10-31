import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import joblib
import os

# ======================================================
# 1. Load Dataset
# ======================================================
df = pd.read_csv("job_roles.csv")

# Replace these column names according to your dataset
# Example: one column is 'Resume' and another is 'Category'
X = df["Resume"]   # features
y = df["Category"] # labels

# ======================================================
# 2. Preprocess Text (Optional: basic cleaning)
# ======================================================
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vectors = vectorizer.fit_transform(X)

# ======================================================
# 3. Split Data
# ======================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_vectors, y, test_size=0.2, random_state=42
)

# ======================================================
# 4. Train CatBoost Model
# ======================================================
model = CatBoostClassifier(
    iterations=300,
    depth=6,
    learning_rate=0.1,
    loss_function='MultiClass',  # <-- changed
    eval_metric='Accuracy',      # <-- changed
    verbose=50,
    train_dir='catboost_info'
)
model.fit(X_train, y_train, eval_set=(X_test, y_test))

# ======================================================
# 5. Evaluate Model
# ======================================================
accuracy = model.score(X_test, y_test)
print(f"\n✅ Model training complete! Accuracy: {accuracy:.4f}")

# ======================================================
# 6. Save Model and Vectorizer
# ======================================================
os.makedirs("models", exist_ok=True)
model.save_model("models/resume_model.cbm")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("📦 Model and vectorizer saved successfully!")

# ======================================================
