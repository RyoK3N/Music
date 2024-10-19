# audio_processing.py
# Audio Processing Module using Pedalboard

import os
import numpy as np
import soundfile as sf
from pedalboard import Pedalboard, Reverb, Compressor


def apply_effects(audio_ar, sr, effects):
    """
    Apply selected effects to the audio array.
    """
    board = Pedalboard()
    if effects.get("reverb"):
        room_size = effects.get("room_size", 0.9)
        board.append(Reverb(room_size=room_size))
    if effects.get("compressor"):
        threshold = effects.get("threshold", -24.0)
        ratio = effects.get("ratio", 2.0)
        board.append(Compressor(threshold_db=threshold, ratio=ratio))
    # Apply the effects
    effected = board(audio_ar, sr)
    return effected


def process_audio(file_path, effects):
    """
    Load an audio file, apply selected effects, and return processed data.
    """
    audio_ar, sr = load_audio(file_path)
    processed_audio = apply_effects(audio_ar, sr, effects)
    return processed_audio, sr


def save_wav(audio_ar, sample_rate, file_name):
    """
    Save the processed audio array to a WAV file.
    """
    base_path = "./recordings"
    file_path = os.path.join(base_path, file_name)
    # Transpose audio_ar to shape (samples, channels)
    audio_ar = audio_ar.T
    sf.write(file_path, audio_ar, sample_rate, subtype="PCM_24")


def load_audio(file_path):
    """
    Load an audio file and return audio array and sample rate.
    """
    audio_ar, sr = sf.read(file_path, dtype="float32", always_2d=True)
    audio_ar = audio_ar.T  # Now shape is (channels, samples)
    return audio_ar, sr
