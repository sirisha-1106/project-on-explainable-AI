import tkinter as tk
import numpy as np
import os
import vlc
import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# ---------------- BASE PATH ----------------
base_path = os.path.dirname(os.path.abspath(__file__))

# ---------------- USER DATA ----------------
blocked_reels = set()

after_id = None

# ---------------- REELS (YOUR ORDER UPDATED) ----------------
reels = [

    {"name": "AI Education", "features": [0.9, 0.1], "harm": 0,
     "video": os.path.join(base_path, "reels", "ai_fixed.mp4")},

    {"name": "Travel Video", "features": [0.6, 0.4], "harm": 0,
     "video": os.path.join(base_path, "reels", "travel_fixed.mp4")},

    {"name": "Python Coding", "features": [0.8, 0.2], "harm": 0,
     "video": os.path.join(base_path, "reels", "coding_fixed.mp4")},

    {"name": "Violent Clip", "features": [0.2, 0.8], "harm": 1,
     "video": os.path.join(base_path, "reels", "violent_fixed.mp4")},

    {"name": "Cricket Highlights", "features": [0.85, 0.15], "harm": 0,
     "video": os.path.join(base_path, "reels", "cricket.mp4")},

    {"name": "Nature Video", "features": [0.7, 0.3], "harm": 0,
     "video": os.path.join(base_path, "reels", "nature.mp4")},

    {"name": "Music Reel", "features": [0.5, 0.5], "harm": 0,
     "video": os.path.join(base_path, "reels", "music.mp4")},

    {"name": "Toxic Reel", "features": [0.1, 0.9], "harm": 1,
     "video": os.path.join(base_path, "reels", "toxic_fixed.mp4")},
]

# ---------------- MODEL ----------------
def build_model():
    model = Sequential([
        Dense(16, activation='relu', input_shape=(2,)),
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

model = build_model()

X_train = np.array([
    [0.9, 0.1],
    [0.8, 0.2],
    [0.6, 0.4],
    [0.2, 0.8],
    [0.1, 0.9],
])
y_train = np.array([1, 1, 1, 0, 0])

model.fit(X_train, y_train, epochs=50, verbose=0)

# ---------------- VLC PLAYER ----------------
class ReelPlayer:
    def __init__(self, frame):
        self.instance = vlc.Instance("--quiet")
        self.player = self.instance.media_player_new()
        self.frame = frame

    def play(self, path):
        if not os.path.exists(path):
            print("❌ Video not found:", path)
            return

        self.player.stop()
        time.sleep(0.2)

        media = self.instance.media_new(path)
        self.player.set_media(media)

        handle = self.frame.winfo_id()
        if os.name == "nt":
            self.player.set_hwnd(handle)
        else:
            self.player.set_xwindow(handle)

        self.player.play()

# ---------------- SIMPLE ORDER (NO AI SORTING) ----------------
def get_recommendations():
    return reels

# ---------------- GLOBAL ----------------
current_index = 0
player = None
current_reel = None

# ---------------- PLAY FUNCTION ----------------
def play_current():
    global current_index, after_id, current_reel

    if after_id:
        root.after_cancel(after_id)

    recs = get_recommendations()

    if current_index >= len(recs):
        current_index = 0

    current_reel = recs[current_index]

    title_label.config(text=current_reel["name"])
    status_label.config(text="▶ Playing reel...")

    player.play(current_reel["video"])

    WATCH_TIME = 8000

    def after_watch():
        global current_index, after_id

        player.player.stop()

        # ⚠️ BLOCK MESSAGE AFTER WATCHING
        if current_reel["harm"] == 1:
            status_label.config(
                text="⚠ Harmful content detected. This reel is now blocked."
            )
            blocked_reels.add(current_reel["name"])
        else:
            status_label.config(text="✔ Reel completed")

        current_index += 1
        after_id = root.after(1200, play_current)

    after_id = root.after(WATCH_TIME, after_watch)

# ---------------- UI ----------------
root = tk.Tk()
root.title("📱 Reel AI System")
root.geometry("400x700")
root.configure(bg="black")

video_frame = tk.Frame(root, bg="black")
video_frame.pack(fill="both", expand=True)

title_label = tk.Label(root, text="", fg="white", bg="black", font=("Arial", 14))
title_label.pack(pady=5)

status_label = tk.Label(root, text="", fg="yellow", bg="black", font=("Arial", 10))
status_label.pack()

# ---------------- CONTROLS ----------------
control_frame = tk.Frame(root, bg="black")
control_frame.pack(pady=10)

def change(step):
    global current_index
    current_index += step
    play_current()

tk.Button(control_frame, text="⬅ Prev", command=lambda: change(-1)).pack(side="left", padx=10)
tk.Button(control_frame, text="Next ➡", command=lambda: change(1)).pack(side="right", padx=10)

# ---------------- START ----------------
player = ReelPlayer(video_frame)
play_current()
root.mainloop()
