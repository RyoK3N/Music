# drum3x.py
# Drum3x - The Ultimate Drum Pad Experience

import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
from ctypes import cdll, c_int
import threading
import time
import os
import sys
import psutil
import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pydub import AudioSegment

# Prevent Pygame from initializing the display module
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Pygame mixer initialization
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

# Loading the compiled C library with error handling
try:
    if sys.platform.startswith("win"):
        lib = cdll.LoadLibrary("drum3x.dll")
    else:
        lib = cdll.LoadLibrary("./libdrum3x.so")
except OSError as e:
    print(f"Error loading C library: {e}")
    sys.exit(1)

# Setting up the C function prototypes
lib.start_recording.restype = None
lib.stop_recording.restype = None
lib.record_beat.argtypes = [c_int]
lib.record_beat.restype = None
lib.get_recording_length.restype = c_int
lib.get_recorded_beat_id.argtypes = [c_int]
lib.get_recorded_beat_id.restype = c_int
lib.get_recorded_beat_timestamp.argtypes = [c_int]
lib.get_recorded_beat_timestamp.restype = c_int

# Initialize Tkinter
root = tk.Tk()
root.title("Drum3x")
root.configure(bg="#0f0f0f")  # Dark background

# Preparing the beats
beat_filenames = [
    "Bass_Drum_Comb.wav",
    "Bass_Drum_Driven12.wav",
    "OH_Open_Hat_04.wav",
    "Bass_Drum_Driven.wav",
    "CH_Closed_Hat23.wav",
    "SD_Snare_Drum_014.wav",
    "Bass_Drum_Driven1.wav",
    "LT_Low_Tom_06.wav",
    "SD_Snare_Drum_092.wav",
]

# Loading beats with error handling
beat_sounds = []
for filename in beat_filenames:
    filepath = os.path.join("beats", filename)
    if not os.path.exists(filepath):
        messagebox.showerror("Error", f"Beat file not found: {filepath}")
        sys.exit(1)
    try:
        beat_sound = pygame.mixer.Sound(filepath)
        beat_sounds.append(beat_sound)
    except pygame.error as e:
        messagebox.showerror("Error", f"Error loading {filepath}: {e}")
        sys.exit(1)


def play_beat(beat_id):
    beat_sounds[beat_id].play()
    lib.record_beat(c_int(beat_id))
    animate_button(beat_id)


def animate_button(beat_id):
    # Change the button style to indicate it's pressed
    buttons[beat_id].config(style="Neon.TButton")
    root.after(100, lambda: buttons[beat_id].config(style="Dark.TButton"))


# Function to start recording
def start_recording():
    lib.start_recording()
    status_label.config(text="Recording...")


# Function to stop recording
def stop_recording():
    lib.stop_recording()
    status_label.config(text="Stopped")


# Function to save recording
def save_recording():
    try:
        recording_length = lib.get_recording_length()
        if recording_length == 0:
            status_label.config(text="No recording to save")
            return

        # Create a silent audio segment with appropriate duration
        last_timestamp = lib.get_recorded_beat_timestamp(c_int(recording_length - 1))
        total_duration = last_timestamp + 1000  # Add 1 second buffer
        mixed = AudioSegment.silent(duration=total_duration)

        for i in range(recording_length):
            beat_id = lib.get_recorded_beat_id(c_int(i))
            timestamp = lib.get_recorded_beat_timestamp(c_int(i))
            beat_audio_path = os.path.join("beats", beat_filenames[beat_id])
            beat_audio = AudioSegment.from_wav(beat_audio_path)
            mixed = mixed.overlay(beat_audio, position=timestamp)

        # Ensure recordings directory exists
        os.makedirs("recordings", exist_ok=True)

        # Generate a unique filename based on current timestamp
        timestamp_str = time.strftime("%Y%m%d-%H%M%S")
        filename = f"recording_{timestamp_str}.wav"
        filepath = os.path.join("recordings", filename)

        # Export the mixed audio
        mixed.export(filepath, format="wav")
        status_label.config(text=f"Recording saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save recording: {e}")
        status_label.config(text="Save failed")


# Function to load recordings
def load_recordings():
    try:
        recordings_dir = "recordings"
        if not os.path.exists(recordings_dir):
            messagebox.showerror("Error", "No 'recordings' directory found.")
            return

        recordings = [f for f in os.listdir(recordings_dir) if f.endswith(".wav")]
        if not recordings:
            messagebox.showerror(
                "Error", "No recordings found in 'recordings' directory."
            )
            return

        # Create a new window to list recordings
        load_window = tk.Toplevel(root)
        load_window.title("Load Recording")
        load_window.configure(bg="#0f0f0f")
        load_window.geometry("300x400")

        listbox = tk.Listbox(
            load_window, bg="#1f1f1f", fg="white", selectbackground="#2f2f2f"
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for rec in recordings:
            listbox.insert(tk.END, rec)

        def play_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showerror("Error", "No recording selected.")
                return
            filename = listbox.get(selected[0])
            filepath = os.path.join(recordings_dir, filename)
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.play()
                status_label.config(text=f"Playing {filename}")
                # Optional: Add animation or visual feedback
            except pygame.error as e:
                messagebox.showerror("Error", f"Cannot play {filename}: {e}")
                status_label.config(text="Playback failed")

        def delete_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showerror("Error", "No recording selected.")
                return
            filename = listbox.get(selected[0])
            filepath = os.path.join(recordings_dir, filename)
            try:
                os.remove(filepath)
                listbox.delete(selected[0])
                status_label.config(text=f"Deleted {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete {filename}: {e}")

        # Play and Delete buttons
        button_frame = ttk.Frame(load_window)
        button_frame.pack(pady=10)

        play_btn = ttk.Button(
            button_frame, text="Play", command=play_selected, style="Dark.TButton"
        )
        play_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(
            button_frame, text="Delete", command=delete_selected, style="Dark.TButton"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load recordings: {e}")
        status_label.config(text="Load failed")


# Function to play back recording from C library
def play_recording():
    recording_length = lib.get_recording_length()
    if recording_length == 0:
        status_label.config(text="No recording to play")
        return
    status_label.config(text="Playing recording...")
    playback_thread = threading.Thread(target=playback_function)
    playback_thread.start()


def playback_function():
    try:
        recording_length = lib.get_recording_length()
        start_time = time.time()
        for i in range(recording_length):
            beat_id = lib.get_recorded_beat_id(c_int(i))
            timestamp = lib.get_recorded_beat_timestamp(c_int(i)) / 1000.0
            time_to_wait = (start_time + timestamp) - time.time()
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            beat_sounds[beat_id].play()
            animate_button(beat_id)
        status_label.config(text="Playback finished")
    except Exception as e:
        messagebox.showerror("Error", f"Playback failed: {e}")
        status_label.config(text="Playback failed")


# Binding keys
key_bindings = ["q", "w", "e", "a", "s", "d", "z", "x", "c"]


def key_pressed(event):
    if event.char.lower() in key_bindings:
        beat_id = key_bindings.index(event.char.lower())
        play_beat(beat_id)


root.bind("<KeyPress>", key_pressed)

# Styling
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Dark.TButton",
    background="#1f1f1f",
    foreground="white",
    borderwidth=2,
    focusthickness=3,
    focuscolor="none",
    width=15,
    height=2,
    relief="flat",
)
style.map("Dark.TButton", background=[("active", "#2f2f2f")])

style.configure(
    "Neon.TButton",
    background="#00ff00",  # Bright Green
    foreground="black",
    borderwidth=2,
    focusthickness=3,
    focuscolor="none",
    width=15,
    height=2,
    relief="flat",
)

# Buttons
buttons = []
for i in range(9):
    row = i // 3
    col = i % 3
    button_text = f"Beat {i+1}\n({key_bindings[i].upper()})"
    button = ttk.Button(
        root, text=button_text, command=lambda i=i: play_beat(i), style="Dark.TButton"
    )
    button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    buttons.append(button)

# Grid configuration
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Control, Save, and Load buttons using pack to avoid overlapping
control_frame = ttk.Frame(root)
control_frame.grid(row=3, column=0, columnspan=3, pady=10)

record_button = ttk.Button(
    control_frame, text="Record", command=start_recording, style="Dark.TButton"
)
record_button.pack(side=tk.LEFT, padx=5)

stop_button = ttk.Button(
    control_frame, text="Stop", command=stop_recording, style="Dark.TButton"
)
stop_button.pack(side=tk.LEFT, padx=5)

play_button = ttk.Button(
    control_frame, text="Play", command=play_recording, style="Dark.TButton"
)
play_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(
    control_frame, text="Save", command=save_recording, style="Dark.TButton"
)
save_button.pack(side=tk.LEFT, padx=5)

load_button = ttk.Button(
    control_frame, text="Load", command=load_recordings, style="Dark.TButton"
)
load_button.pack(side=tk.LEFT, padx=5)

status_label = ttk.Label(root, text="Ready", background="#0f0f0f", foreground="white")
status_label.grid(row=4, column=0, columnspan=3, pady=5)

# Real-time CPU usage
cpu_window = tk.Toplevel(root)
cpu_window.title("System Performance Monitor")
cpu_window.configure(bg="#0f0f0f")
cpu_window.geometry("600x400")

# CPU usage plot setup
fig, ax = plt.subplots(facecolor="#0f0f0f")
fig.patch.set_facecolor("#0f0f0f")
ax.set_facecolor("#0f0f0f")
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["left"].set_color("white")
ax.spines["right"].set_color("white")
ax.set_ylabel("CPU Usage (%)", color="white", fontweight="bold")
ax.set_xlabel("Time (s)", color="white", fontweight="bold")
ax.set_title("CPU Utilization", color="white", fontweight="bold")

cpu_usage_data = []
time_data = []
start_time = time.time()


def update_cpu_usage(i):
    current_time = time.time() - start_time
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_usage_data.append(cpu_percent)
    time_data.append(current_time)
    if len(time_data) > 60:
        time_data.pop(0)
        cpu_usage_data.pop(0)
    ax.clear()
    ax.plot(time_data, cpu_usage_data, color="#00ff00", linewidth=2)
    ax.set_ylim(0, 100)
    ax.set_ylabel("CPU Usage (%)", color="white", fontweight="bold")
    ax.set_xlabel("Time (s)", color="white", fontweight="bold")
    ax.set_title("CPU Utilization", color="white", fontweight="bold")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.set_facecolor("#0f0f0f")
    ax.spines["bottom"].set_color("white")
    ax.spines["top"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.spines["right"].set_color("white")
    ax.grid(True, color="#2f2f2f")


canvas = FigureCanvasTkAgg(fig, master=cpu_window)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

ani = animation.FuncAnimation(fig, update_cpu_usage, interval=1000)

root.mainloop()
