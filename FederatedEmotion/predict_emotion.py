import time
import pickle
import numpy as np
from pynput import keyboard

print("Loading Global Emotion Model...")

with open("global_model.pkl", "rb") as f:
    model = pickle.load(f)

press_times = []
release_times = []

def on_press(key):
    press_times.append(time.time())

def on_release(key):
    release_times.append(time.time())
    if key == keyboard.Key.esc:
        return False

print("Start typing to predict emotion...")
print("Press ESC when finished.\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# -------- Feature Calculation --------
hold_times = []
for i in range(min(len(press_times), len(release_times))):
    hold_times.append(release_times[i] - press_times[i])

avg_hold = np.mean(hold_times) if hold_times else 0

inter_delays = []
for i in range(1, len(press_times)):
    inter_delays.append(press_times[i] - release_times[i-1])

avg_delay = np.mean(inter_delays) if inter_delays else 0

typing_speed = len(press_times) / sum(hold_times) if sum(hold_times) != 0 else 0
error_rate = 0
total_keys = len(press_times)

import pandas as pd

X = pd.DataFrame([[
    avg_hold,
    typing_speed,
    avg_delay,
    error_rate,
    total_keys
]], columns=[
    "avg_hold_time",
    "typing_speed",
    "avg_interkey_delay",
    "error_rate",
    "total_keys"
])

emotion = model.predict(X)[0]

print("\nPredicted Emotion →", emotion)