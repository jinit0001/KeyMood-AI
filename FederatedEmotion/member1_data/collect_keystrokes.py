import time
import os
from pynput import keyboard
import pandas as pd

# ----------- Storage Variables -----------
press_time = {}
hold_times = []
inter_key_delays = []

last_release_time = None
backspace_count = 0
total_keys = 0

# ----------- Key Press Event -----------
def on_press(key):
    global backspace_count, total_keys

    press_time[key] = time.time()
    total_keys += 1

    if key == keyboard.Key.backspace:
        backspace_count += 1


# ----------- Key Release Event -----------
def on_release(key):
    global last_release_time

    if key in press_time:
        release_time = time.time()
        hold = release_time - press_time[key]
        hold_times.append(hold)

        if last_release_time is not None:
            delay = press_time[key] - last_release_time
            inter_key_delays.append(delay)

        last_release_time = release_time

    if key == keyboard.Key.esc:
        return False


# ----------- Start Recording -----------
print("\nStart typing... Press ESC to stop.")
print("NOTE: Actual typed characters are NOT stored for privacy.\n")

start_time = time.time()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

end_time = time.time()

# ----------- Feature Calculation -----------
typing_duration = end_time - start_time

typing_speed = total_keys / typing_duration if typing_duration > 0 else 0

avg_hold_time = sum(hold_times) / len(hold_times) if hold_times else 0
avg_delay = sum(inter_key_delays) / len(inter_key_delays) if inter_key_delays else 0

error_rate = backspace_count / total_keys if total_keys > 0 else 0

# ----------- Emotion Label -----------
emotion = input("Enter emotion (calm / happy / stressed / neutral): ").lower()

# ----------- Create DataFrame -----------
session_data = pd.DataFrame([{
    "avg_hold_time": avg_hold_time,
    "avg_interkey_delay": avg_delay,
    "typing_speed": typing_speed,
    "error_rate": error_rate,
    "total_keys": total_keys,
    "emotion": emotion
}])

# ----------- Auto Folder Creation -----------
save_folder = "../data/raw"
os.makedirs(save_folder, exist_ok=True)

file_path = os.path.join(save_folder, "keystroke_sessions.csv")

# ----------- Save CSV -----------
session_data.to_csv(
    file_path,
    mode="a",
    header=not os.path.exists(file_path),
    index=False
)

print("\nSession saved successfully ✅")
print("Saved at:", file_path)

# ----------- Show Summary -----------
print("\nSession Summary")
print("---------------------")
print("Typing Speed:", round(typing_speed, 2))
print("Average Hold Time:", round(avg_hold_time, 4))
print("Average Inter-Key Delay:", round(avg_delay, 4))
print("Error Rate:", round(error_rate, 3))
print("Total Keys:", total_keys)