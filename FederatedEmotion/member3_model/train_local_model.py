import pandas as pd
import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

print("\nLoading features dataset...")

data_path = "../data/processed/features.csv"

# ---------- Dataset Check ----------
if not os.path.exists(data_path):
    print("❌ ERROR: features.csv not found. Run feature extraction first.")
    exit()

data = pd.read_csv(data_path)

# ---------- Clean Data ----------
data = data.replace([float("inf"), float("-inf")], pd.NA)
data = data.dropna()

print(f"Dataset Loaded → {len(data)} samples")

# ---------- Data Requirements ----------
if len(data) < 10:
    print("❌ ERROR: Collect at least 10–15 sessions.")
    exit()

if data["emotion"].nunique() < 2:
    print("❌ ERROR: Need multiple emotions.")
    exit()

# ---------- Features ----------
features = [
    "avg_hold_time",
    "typing_speed",
    "avg_interkey_delay",
    "error_rate",
    "total_keys"
]

X = data[features]
y = data["emotion"]

# ---------- Stratified Split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# ---------- Model ----------
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=3000, class_weight="balanced"))
])

print("Training model...")
model.fit(X_train, y_train)

# ---------- Evaluation ----------
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy → {acc:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ---------- Save ----------
model_path = "../local_model.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"\nModel saved at → {model_path}")
print("✅ Training COMPLETE\n")