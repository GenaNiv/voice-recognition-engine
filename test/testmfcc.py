import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from feature_extraction.audio_feature_extractor import AudioFeatureExtractor

# Compare MFCCs and generate images for both custom and librosa methods
def compare_mfcc_methods(file_path):
    # 1. Load the signal
    signal, sample_rate = librosa.load(file_path, sr=None)

    # 2. Extract MFCCs using custom method
    customer_mfcc = AudioFeatureExtractor(signal, sample_rate)
    custom_mfcc = customer_mfcc.extract_features(signal, sample_rate)

    # 3. Extract MFCCs using librosa method
    n_fft = 512
    hop_length = 160
    librosa_mfcc = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=13, n_fft=n_fft, hop_length=hop_length)

    # 4. Plot the custom MFCC
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    librosa.display.specshow(custom_mfcc.T, sr=sample_rate, hop_length=hop_length, x_axis='time')
    plt.colorbar()
    plt.title("Custom MFCC")
    plt.xlabel("Time")
    plt.ylabel("MFCC Coefficients")

    # 5. Plot the librosa MFCC
    plt.subplot(1, 2, 2)
    librosa.display.specshow(librosa_mfcc, sr=sample_rate, hop_length=hop_length, x_axis='time')
    plt.colorbar()
    plt.title("Librosa MFCC")
    plt.xlabel("Time")
    plt.ylabel("MFCC Coefficients")

    plt.tight_layout()
    plt.savefig('mfcc_comparison.png')  # Save the comparison plot as an image
    plt.show()

if __name__ == "__main__":
    compare_mfcc_methods('gena.wav')
