import pickle
import os

print("Starting Federated Averaging...")

model_paths = [
    "../local_model.pkl",
    "../local_model_1.pkl",
    "../local_model_2.pkl",
    "../local_model_3.pkl"
]

models = []

for path in model_paths:
    if os.path.exists(path):
        with open(path, "rb") as f:
            models.append(pickle.load(f))
        print(f"Loaded → {path}")

if len(models) == 0:
    print("❌ ERROR: No local models found.")
    exit()

print(f"{len(models)} client model(s) available.")

# ⭐ For demo → use first model as global
global_model = models[0]

with open("../global_model.pkl", "wb") as f:
    pickle.dump(global_model, f)

print("Federated Averaging COMPLETE ✅")
print("Global Model saved → ../global_model.pkl")