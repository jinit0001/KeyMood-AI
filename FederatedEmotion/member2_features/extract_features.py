import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

print("Starting Feature Extraction...")

# -------- File Path --------
raw_path = "../data/raw/keystroke_sessions.csv"

# -------- Check File Exists --------
if not os.path.exists(raw_path):
    print("❌ ERROR: Raw data file not found!")
    print("👉 Run collect_keystrokes.py first")
    exit()

# -------- Load Data --------
df = pd.read_csv(raw_path)

print("Raw dataset loaded successfully ✅")
print(df.head())

# -------- Check Data --------
if df.empty:
    print("❌ ERROR: Dataset is empty!")
    exit()

if "emotion" not in df.columns:
    print("❌ ERROR: 'emotion' column missing!")
    exit()

# -------- Remove Missing Values --------
df = df.dropna()

# -------- Separate Features --------
X = df.drop("emotion", axis=1)
y = df["emotion"]

# -------- Check Feature Columns --------
if X.shape[1] == 0:
    print("❌ ERROR: No feature columns found!")
    exit()

# -------- Normalization --------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------- Convert Back to DataFrame --------
df_features = pd.DataFrame(X_scaled, columns=X.columns)
df_features["emotion"] = y.values

# -------- Save Processed Data --------
save_folder = "../data/processed"
os.makedirs(save_folder, exist_ok=True)

save_path = os.path.join(save_folder, "features.csv")
df_features.to_csv(save_path, index=False)

print("\n✅ Feature Extraction COMPLETE")
print("Saved at:", save_path)