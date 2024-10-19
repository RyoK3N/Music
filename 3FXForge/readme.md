# 3FXForge - Audio Processing Suite

## Overview

3FXForge is a Python-based graphical audio processing application that allows you to load, play, and process WAV recordings with audio effects. The application provides interactive controls for playback and lets you apply effects like Reverb and Compression to your recordings. 


## Features

Load Recordings: Automatically load WAV files from the recordings directory.

Playback Controls: Play, pause, stop, and navigate through recordings.

### Effects:
```css
Reverb: Adds Reverb Sound Effect to the Audio.

Compressor: Compresses the Audio based on a threshold.

Save Processed Audio: Save your processed recordings as new WAV files.

CPU Usage Monitoring: Separate window displaying CPU usage.
```
## Installation
### Prerequisites
      Python 3.6 or higher
      pip 24.2
  
### Clone the Repository
```bash
git clone https://github.com/yourusername/3FXForge.git
cd 3FXForge
```
### If requirements.txt in 3FXForge :
``` bash
pip install -r requirements.txt
```
### else :

```bash
pip install psutil numpy soundfile simpleaudio pedalboard
```
Note: On some systems, additional system packages may be required for soundfile and simpleaudio.

1. Prepare Recordings Directory
Ensure there's a recordings directory in the project root. Place your WAV audio files into this directory. If the directory doesn't exist, the application will create it upon running.

2. Run the Application
```bash
python gui_application.py
```

3. Loading Recordings
The application auto-loads WAV files from the recordings directory at startup.
To refresh the list manually, click the Load Recordings button.
4. Playback Controls
Select a Recording: Click on a recording in the list to select it.
Play/Pause: Click the Play button to start or pause playback.
Stop: Click the Stop button to halt playback.
Previous/Next: Use the Prev and Next buttons to navigate recordings.
5. Applying Effects
Reverb
Enable: Check the Reverb checkbox.
Adjust Room Size: Set the Room Size parameter (default is 0.9).
Compressor
Enable: Check the Compressor checkbox.
Adjust Threshold: Set the Threshold (dB) parameter (default is -24.0).
Adjust Ratio: Set the Ratio parameter (default is 2.0).
Apply Effects
Click the Apply Effects button to process the selected recording with the chosen effects.
A message will confirm when processing is complete.
6. Playing Processed Audio
After applying effects, use the playback controls to listen to the processed audio.
7. Saving Processed Audio
Click the Save Processed button.
Choose a filename and location in the dialog that appears.
The processed audio will be saved as a WAV file.
8. CPU Usage Monitoring
A separate window displays real-time CPU usage.
This window updates every second and can help monitor the application's performance.

### File Structure
gui_application.py: Main GUI application script.
audio_processing.py: Audio processing module using Pedalboard.
recordings/: Directory containing WAV recordings.
requirements.txt: List of Python package dependencies.

### Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for suggestions and improvements.

## License
This project is licensed under the MIT License.

## Acknowledgments
Pedalboard by Spotify for the audio effects processing library.
Tkinter for the GUI framework.
Community Contributors for their valuable input and improvements.
