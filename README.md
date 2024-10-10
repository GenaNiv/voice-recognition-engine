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
3. **List Enrolled Speakers**: Display a list of all enrolled speakers.
4. **Delete a Speaker**: Remove a speaker's data from the system.

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
