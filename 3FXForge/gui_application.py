# gui_application.py
# GUI Application for 3FXForge with Interactive Buttons and Progress Bar

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import psutil
import numpy as np
from audio_processing import process_audio, save_wav, load_audio, apply_effects
import simpleaudio as sa
import time


class FXForgeApp:
    def __init__(self, master):
        self.master = master
        master.title("3FXForge - Audio Processing Suite")
        master.geometry("800x600")
        master.configure(bg="#1e1e1e")

        # Style Configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", foreground="white", background="#333333")
        style.map(
            "TButton",
            foreground=[("active", "white")],
            background=[("active", "#555555")],
        )
        style.configure("TLabel", foreground="white", background="#1e1e1e")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TRadiobutton", foreground="white", background="#1e1e1e")
        style.configure("TCheckbutton", foreground="white", background="#1e1e1e")

        # Status Label
        status_frame = ttk.Frame(master)
        status_frame.pack(pady=10)

        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack()

        # Recording List
        list_frame = ttk.Frame(master)
        list_frame.pack(fill=tk.X, padx=20)

        self.listbox = tk.Listbox(
            list_frame,
            bg="#2e2e2e",
            fg="white",
            selectbackground="#444444",
            selectforeground="white",
            height=5,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Control Buttons
        control_frame = ttk.Frame(master)
        control_frame.pack(pady=10)

        prev_button = ttk.Button(control_frame, text="Prev", command=self.prev_track)
        prev_button.grid(row=0, column=0, padx=5)

        self.play_pause_button = ttk.Button(
            control_frame, text="Play", command=self.play_pause_recording
        )
        self.play_pause_button.grid(row=0, column=1, padx=5)

        stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_playback)
        stop_button.grid(row=0, column=2, padx=5)

        next_button = ttk.Button(control_frame, text="Next", command=self.next_track)
        next_button.grid(row=0, column=3, padx=5)

        load_button = ttk.Button(
            control_frame, text="Load Recordings", command=self.load_recordings
        )
        load_button.grid(row=0, column=4, padx=5)

        process_button = ttk.Button(
            control_frame, text="Apply Effects", command=self.apply_effects_button
        )
        process_button.grid(row=0, column=5, padx=5)

        save_button = ttk.Button(
            control_frame, text="Save Processed", command=self.save_recording
        )
        save_button.grid(row=0, column=6, padx=5)

        # Processing Options
        process_frame = ttk.LabelFrame(
            master, text="Processing Options", style="TFrame"
        )
        process_frame.pack(pady=10, padx=20, fill=tk.X)

        # Reverb Option
        self.reverb_var = tk.BooleanVar()
        reverb_cb = ttk.Checkbutton(
            process_frame, text="Reverb", variable=self.reverb_var
        )
        reverb_cb.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.room_size_var = tk.DoubleVar(value=0.9)
        room_size_label = ttk.Label(process_frame, text="Room Size:")
        room_size_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        room_size_entry = ttk.Entry(
            process_frame, textvariable=self.room_size_var, width=5
        )
        room_size_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Compressor Option
        self.compressor_var = tk.BooleanVar()
        compressor_cb = ttk.Checkbutton(
            process_frame, text="Compressor", variable=self.compressor_var
        )
        compressor_cb.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.threshold_var = tk.DoubleVar(value=-24.0)
        threshold_label = ttk.Label(process_frame, text="Threshold (dB):")
        threshold_label.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        threshold_entry = ttk.Entry(
            process_frame, textvariable=self.threshold_var, width=5
        )
        threshold_entry.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.ratio_var = tk.DoubleVar(value=2.0)
        ratio_label = ttk.Label(process_frame, text="Ratio:")
        ratio_label.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        ratio_entry = ttk.Entry(process_frame, textvariable=self.ratio_var, width=5)
        ratio_entry.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        # Progress Bar and Time Label
        progress_frame = ttk.Frame(master)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.time_label = ttk.Label(
            progress_frame,
            text="00:00 / 00:00",
            foreground="white",
            background="#1e1e1e",
        )
        self.time_label.pack(side=tk.RIGHT, padx=10)

        # CPU Usage Monitoring
        self.cpu_window = tk.Toplevel(master)
        self.cpu_window.title("CPU Usage Monitor")
        self.cpu_window.geometry("300x100")
        self.cpu_window.configure(bg="#1e1e1e")

        self.cpu_label = ttk.Label(
            self.cpu_window,
            text="CPU Usage: 0%",
            foreground="white",
            background="#1e1e1e",
            font=("Helvetica", 16),
        )
        self.cpu_label.pack(pady=20)

        self.update_cpu_usage()

        # Variables
        self.is_playing = False
        self.is_paused = False
        self.current_index = 0
        self.recordings = []
        self.load_recordings()

        self.play_obj = None
        self.audio_data = None
        self.sample_rate = None
        self.playback_position = 0
        self.processed_audio = None  # Holds processed audio data

    def update_cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
        self.master.after(1000, self.update_cpu_usage)

    def load_recordings(self):
        """
        Load WAV recordings from the 'recordings' directory.
        """
        self.recordings = []
        recordings_dir = "recordings"
        if not os.path.exists(recordings_dir):
            os.makedirs(recordings_dir)
            self.status_label.config(text="Created 'recordings' directory.")

        self.recordings = [
            f for f in os.listdir(recordings_dir) if f.lower().endswith(".wav")
        ]
        self.recordings.sort()
        self.listbox.delete(0, tk.END)
        for rec in self.recordings:
            self.listbox.insert(tk.END, rec)
        self.status_label.config(text=f"Loaded {len(self.recordings)} recordings.")
        if self.recordings:
            self.listbox.selection_set(0)
            self.on_select(None)

    def on_select(self, event):
        """
        Event handler for listbox selection.
        """
        selected = self.listbox.curselection()
        if selected:
            self.current_index = selected[0]
            filename = self.recordings[self.current_index]
            self.status_label.config(text=f"Selected {filename}")
            # Discard processed audio when a new file is selected
            self.processed_audio = None
            self.processed_sample_rate = None

    def play_pause_recording(self):
        if self.is_playing and not self.is_paused:
            # Pause playback
            if self.play_obj:
                self.play_obj.stop()
            self.is_paused = True
            self.play_pause_button.config(text="Play")
            self.status_label.config(text="Paused")
        elif self.is_playing and self.is_paused:
            # Resume playback
            self.is_paused = False
            self.play_pause_button.config(text="Pause")
            self.status_label.config(text="Playing")
            threading.Thread(target=self.start_playback_from_position).start()
        else:
            # Start playback
            selected = self.listbox.curselection()
            if not selected:
                messagebox.showerror("Error", "No recording selected.")
                return
            filename = self.recordings[selected[0]]
            filepath = os.path.join("recordings", filename)
            self.status_label.config(text=f"Playing {filename}")
            try:
                threading.Thread(target=self.start_playback).start()
                self.play_pause_button.config(text="Pause")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot play {filename}: {e}")
                self.status_label.config(text="Playback failed")

    def start_playback(self):
        self.is_playing = True
        self.is_paused = False
        self.playback_position = 0

        # Use processed audio if available
        if self.processed_audio is not None:
            self.audio_data = self.processed_audio
            self.sample_rate = self.processed_sample_rate
        else:
            selected = self.listbox.curselection()
            filename = self.recordings[selected[0]]
            filepath = os.path.join("recordings", filename)
            self.audio_data, self.sample_rate = load_audio(filepath)

        self.audio_length = self.audio_data.shape[1] / self.sample_rate
        self.start_playback_from_position()

    def start_playback_from_position(self):
        def playback():
            remaining_data = self.audio_data[
                :, int(self.playback_position * self.sample_rate) :
            ]
            if remaining_data.size == 0:
                self.is_playing = False
                self.play_pause_button.config(text="Play")
                self.status_label.config(text="Playback finished.")
                self.progress_var.set(0)
                self.time_label.config(text="00:00 / 00:00")
                return
            data_to_play = (remaining_data.T * 32767).astype(np.int16)
            # Ensure data is C-contiguous
            data_to_play = np.ascontiguousarray(data_to_play)
            self.play_obj = sa.play_buffer(
                data_to_play,
                num_channels=self.audio_data.shape[0],
                bytes_per_sample=2,
                sample_rate=self.sample_rate,
            )
            start_time = time.time() - self.playback_position
            while self.play_obj.is_playing():
                if self.is_paused or not self.is_playing:
                    self.play_obj.stop()
                    break
                current_time = time.time() - start_time
                progress = (current_time / self.audio_length) * 100
                self.progress_var.set(progress)
                # Update time label
                elapsed = time.strftime("%M:%S", time.gmtime(current_time))
                total = time.strftime("%M:%S", time.gmtime(self.audio_length))
                self.time_label.config(text=f"{elapsed} / {total}")
                time.sleep(0.1)
            self.is_playing = False
            self.play_pause_button.config(text="Play")
            self.status_label.config(text="Playback finished.")
            self.progress_var.set(0)
            self.time_label.config(text="00:00 / 00:00")

        threading.Thread(target=playback).start()

    def apply_effects_button(self):
        """
        Apply effects and store processed audio in memory.
        """
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No recording selected.")
            return
        filename = self.recordings[selected[0]]
        filepath = os.path.join("recordings", filename)
        self.status_label.config(text=f"Processing {filename}...")

        # Gather selected effects
        effects = self.get_selected_effects()
        if not effects:
            messagebox.showerror("Error", "No effects selected.")
            self.status_label.config(text="No effects selected.")
            return

        # Start processing in a new thread to keep GUI responsive
        processing_thread = threading.Thread(
            target=self.apply_effects_in_memory, args=(filepath, effects)
        )
        processing_thread.start()

    def apply_effects_in_memory(self, filepath, effects):
        """
        Apply effects and store the processed audio in memory.
        """
        try:
            processed_data, sample_rate = process_audio(filepath, effects)
            self.processed_audio = processed_data
            self.processed_sample_rate = sample_rate
            self.master.after(0, self.show_processing_success)
        except Exception as e:
            self.master.after(0, self.show_error_message, e)

    def show_processing_success(self):
        messagebox.showinfo(
            "Success", "Effects applied. You can now play the processed audio."
        )
        self.status_label.config(text="Effects applied. Ready to play.")

    def stop_playback(self):
        self.is_playing = False
        self.is_paused = False
        self.playback_position = 0
        if self.play_obj:
            self.play_obj.stop()
        self.progress_var.set(0)
        self.play_pause_button.config(text="Play")
        self.status_label.config(text="Playback stopped.")
        self.time_label.config(text="00:00 / 00:00")

    def prev_track(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.on_select(None)
            self.stop_playback()
            self.play_pause_recording()

    def next_track(self):
        if self.current_index < len(self.recordings) - 1:
            self.current_index += 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.on_select(None)
            self.stop_playback()
            self.play_pause_recording()

    def get_selected_effects(self):
        """
        Get the effects selected by the user.
        """
        effects = {}
        if self.reverb_var.get():
            effects["reverb"] = True
            effects["room_size"] = self.room_size_var.get()
        if self.compressor_var.get():
            effects["compressor"] = True
            effects["threshold"] = self.threshold_var.get()
            effects["ratio"] = self.ratio_var.get()
        return effects

    def apply_effects_and_save(self):
        """
        Apply effects and save processed audio to a file.
        """
        if self.processed_audio is None:
            messagebox.showerror(
                "Error", "No processed audio available. Please apply effects first."
            )
            return
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No recording selected.")
            return
        filename = self.recordings[selected[0]]
        processed_filename = f"processed_{filename}"
        save_wav(self.processed_audio, self.processed_sample_rate, processed_filename)
        self.status_label.config(text=f"Processed audio saved as {processed_filename}")
        self.load_recordings()

    def show_error_message(self, error):
        messagebox.showerror("Error", f"Failed to process audio: {error}")
        self.status_label.config(text="Processing failed.")

    def save_recording(self):
        """
        Save the processed recording to a different location.
        """
        if self.processed_audio is None:
            messagebox.showerror(
                "Error", "No processed audio to save. Please apply effects first."
            )
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            initialfile="processed_audio.wav",
        )
        if save_path:
            try:
                audio_ar = (
                    self.processed_audio.T
                )  # Transpose back to (samples, channels)
                sa.write(
                    save_path, audio_ar, self.processed_sample_rate, subtype="PCM_24"
                )
                self.status_label.config(text=f"Processed audio saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
                self.status_label.config(text="Save failed.")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FXForgeApp(root)
    root.mainloop()
