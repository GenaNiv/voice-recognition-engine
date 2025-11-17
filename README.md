# Speaker Recognition Engine

The Speaker Recognition Engine is a command-line tool for managing speaker audio data. It supports the following functionalities:
- Enrolling new speakers
- Recognizing speakers from audio samples
- Listing all enrolled speakers
- Deleting speaker records

The engine leverages machine learning techniques, specifically Gaussian Mixture Models (GMM), 
to perform accurate and robust speaker identification.

## Installation
1. **Clone the Repository**
   ```bash
   git clone git@github.com:GenaNiv/voice-recognition-engine.git
   cd voice-recognition-engine

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

3. **Verify the Installation**
   ```bash
   python cli.py --help

## Usage

The Speaker Recognition Engine supports several commands for managing speaker audio data. Below are the available commands:

1. **Enroll a Speaker**: Enroll a new speaker using an audio file.
2. **Recognize a Speaker**: Identify a speaker from a given audio file.
3. **Recognize a Stream**: Feed audio chunks in near real-time and observe interim matches.
4. **List Enrolled Speakers**: Display a list of all enrolled speakers.
5. **Delete a Speaker**: Remove a speaker's data from the system.

Each command can be executed from the command line with the appropriate arguments. 
The general syntax for using the tool is:
```bash
python cli.py <command> [arguments]
```

## Enroll a Speaker

To enroll a new speaker, use the `enroll` command followed by the speaker's name and the path to the audio file. Optionally, you can specify parameters like sample rate, number of filters, and number of MFCC coefficients.

**Syntax:**
```bash
python cli.py enroll <speaker_name> <audio_file_path> [optional parameters]
```
**Optional Parameters:**
- `--sample_rate`: Sampling rate of the audio file (default: `16000`)
- `--num_filters`: Number of Mel filters (default: `26`)
- `--num_ceps`: Number of MFCC coefficients (default: `13`)
- `--n_fft`: FFT size for audio processing (default: `512`)
- `--frame_size`: Frame size in seconds (default: `0.025`)
- `--frame_step`: Frame step (overlap) in seconds (default: `0.01`)
- `--n_mixtures`: Number of Gaussian mixtures in GMM (default: `8`)


**Example:**
```bash
python cli.py enroll gena /home/gena/audio_files/gena.wav --sample_rate 16000 --num_filters 40 --num_ceps 13 --n_fft 512 --frame_size 0.025 --frame_step 0.01 --n_mixtures 8
```

## Recognize a Speaker

Run the `recognize` command with a wav file. The CLI prints the best match and log-likelihood scores that come from the shared `VoiceRecognitionService`.

```bash
python cli.py recognize /home/gena/audio_files/gena.wav --sample_rate 16000
```

## Recognize a Stream (Real-Time Simulation)

The `recognize_stream` command reuses the same service façade but feeds the audio file in chunks (default 0.5 s). This mimics real-time capture and prints interim matches as soon as the likelihoods are high enough.

```bash
python cli.py recognize_stream /home/gena/audio_files/gena.wav --chunk_duration 0.25
```

## Live Microphone Demo

Use `src/live_recognition.py` to capture audio from the default input device and route it directly through the streaming API. Ensure `sounddevice` sees your microphone, then run:

```bash
python src/live_recognition.py
```

Speak into the microphone—interim matches will appear as the engine accumulates enough audio. Press `Ctrl+C` to stop.

## Embedding the Service API

For tighter integration with other applications (e.g., the upcoming voice engine), import `VoiceRecognitionService` and the request/response models:

```python
from file_management.bst import BinarySearchTree
from service.api import VoiceRecognitionService, EnrollmentRequest, EnrollmentConfig
from service.audio_sources import BufferAudioSource

bst = BinarySearchTree()
service = VoiceRecognitionService(bst=bst, base_directory="test_environment")

# Enroll using in-memory buffers
req = EnrollmentRequest(
    speaker_id="alice",
    audio_source=BufferAudioSource(buffers=[pcm_chunk_1, pcm_chunk_2]),
    config=EnrollmentConfig(sample_rate=16000),
)
service.enroll(req)
```

The same façade exposes `recognize`, `start_session`, `list_speakers`, and `delete_speaker`, allowing other repositories to depend on this module without invoking the CLI.

## Recording a Test WAV on Raspberry Pi with Jabra Speak 410

Use this workflow to capture a 16 kHz mono WAV file on the Raspberry Pi 5 connected to the Jabra speaker/mic. All commands assume the repository lives under `/home/gena/PROJECTS`.

1. Set the Jabra device as the default PipeWire sink/source:
   ```bash
   ./roomba_stack/audio_jabra_default.sh
   ```
2. Confirm the capture device name (needed in the next step):
   ```bash
   pactl list short sources | grep -i jabra
   ```
   You should see something like `alsa_input.usb-0b0e_Jabra_SPEAK_410_USB_...-mono-fallback` running at 16 kHz.
3. Make sure there is a place to store recordings:
   ```bash
   mkdir -p voice-recognition-engine/audio_files
   ```
4. Record a short sample (5–10 seconds) using the PipeWire/ALSA device discovered in step 2:
   ```bash
   parecord \
     --device=alsa_input.usb-0b0e_Jabra_SPEAK_410_USB_50C2ED166881x011200-00.mono-fallback \
     --rate=16000 --channels=1 --format=s16le \
     voice-recognition-engine/audio_files/gmm_test.wav
   ```
   Speak while the command runs and press `Ctrl+C` when finished.
5. Validate the recording before using it with the GMM engine:
   ```bash
   aplay voice-recognition-engine/audio_files/gmm_test.wav
   ```

The resulting `gmm_test.wav` resides in `voice-recognition-engine/audio_files/` and can be supplied to the CLI commands (e.g., `python src/cli.py recognize voice-recognition-engine/audio_files/gmm_test.wav --sample_rate 16000`).
