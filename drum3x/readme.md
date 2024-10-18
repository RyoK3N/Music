# Drum3x

Welcome to **Drum3x**, the ultimate drum pad experience! Drum3x transforms your keyboard into a dynamic drum machine with a sleek, gaming-inspired interface. Whether you're a budding musician or just looking to have some fun, Drum3x offers an engaging platform to unleash your rhythm skills.

## Features

- 🎹 **9 Dynamic Drum Pads**: A 3x3 grid of responsive pads, each linked to unique drum sounds.
- 💻 **Keyboard Integration**: Play beats effortlessly using intuitive keyboard shortcuts.
- 🎶 **Record & Playback**: Capture your creative sequences and replay them with precise timing.
- 🎮 **Gaming-Inspired UI**: Immerse yourself in a dark-themed interface with neon highlights and a real-time CPU utilization graph styled like a gaming HUD.
- 📈 **System Performance Monitor**: Keep an eye on your system's performance with a live-updating, gaming-styled CPU usage graph.

Drum3x is more than just a drum pad—it's a glimpse into a larger project aimed at redefining interactive music experiences. Stay tuned for exciting updates!

## Installation

### Prerequisites

- **Python 3.x**
- **C Compiler** (e.g., GCC)
- **Pip** (Python package manager)

### Python Packages

Install the required Python packages using pip:

```bash
pip install psutil pygame matplotlib
```

## Prepare Sound Files
__Create a beats Folder:__ Place it in the same directory as your scripts.

__Add Drum Sound Files:__ Ensure you have 9 WAV files in the beats folder with the following filenames:

    --beats\
    ----Bass_Drum_Comb.wav
    ----Bass_Drum_Driven12.wav
    ----OH_Open_Hat_04.wav
    ----Bass_Drum_Driven.wav
    ----CH_Closed_Hat23.wav
    ----SD_Snare_Drum_014.wav
    ----Bass_Drum_Driven1.wav
    ----LT_Low_Tom_06.wav
    ----SD_Snare_Drum_092.wav
Note: The sound files should be in uncompressed 16-bit PCM WAV format. You can convert your audio files using ffmpeg:

```bash
ffmpeg -i input.wav -acodec pcm_s16le -ar 44100 output.wav
```

## Compile the C Library

Compile drum3x.c into a shared library.

__On macOS/Linux:__

```bash
gcc -shared -o libdrum3x.so -fPIC drum3x.c
```
__On Windows:__

```bash
gcc -shared -o drum3x.dll -Wl,--out-implib,libdrum3x.a -Wl,--export-all-symbols -Wl,--enable-auto-import drum3x.c
```
__Usage__

Run the application:
```bash
python drum3x.py
```

__Controls__
Drum Pads: Click on the buttons or use the keyboard keys to play beats.

__Key Bindings:__

```css
Copy code
q w e
a s d
z x c
```

Record: Click the Record button to start recording your beat sequence.

Stop: Click the Stop button to stop recording.

Play: Click the Play button to play back your recorded sequence.

System Performance Monitor: A separate window displays the CPU usage over time with a gaming-inspired graph.

## Screenshots


## Troubleshooting

No Sound: Ensure your sound files are correctly named and placed in the beats folder. Check that they are in the correct format.
Application Crashes: Make sure all dependencies are installed and that you're using compatible versions.
Key Bindings Not Working: Ensure the application window is focused when pressing keys.

## Contribution
Drum3x is part of a larger vision to create interactive and immersive music applications. If you're interested in contributing or have ideas to enhance Drum3x, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
```css
Pygame: For providing a powerful library to handle audio playback.
Matplotlib: For making it easy to embed dynamic graphs in the application.
Psutil: For accessing system performance metrics.
Community: Thanks to everyone who has inspired and supported this project.
Unleash your inner rhythm and take the first step into an exciting musical journey with Drum3x!
```
