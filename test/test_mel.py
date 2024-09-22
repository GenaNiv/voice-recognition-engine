import librosa
import numpy as np
from mel_filterbank import MelScaleFilterbank

# Import the custom MelScaleFilterbank class
# (Assume it has already been defined or imported)

# Parameters
sample_rate = 16000
n_fft = 512
n_mels = 26

# Generate the filterbank using Librosa
mel_librosa = librosa.filters.mel(sr=sample_rate, n_fft=n_fft, n_mels=n_mels)

# Generate the filterbank using our custom implementation
mel_custom = MelScaleFilterbank(num_filters=n_mels, fft_size=n_fft, sample_rate=sample_rate)

# Compare the two filterbanks
print("Librosa Filterbank:\n", mel_librosa)
print("Custom Filterbank:\n", mel_custom.filterbank)

# Check if the difference is within a reasonable threshold
diff = np.abs(mel_librosa - mel_custom.filterbank)
print("Max Difference:", np.max(diff))

# If the max difference is very small, the implementation is correct
if np.max(diff) < 1e-5:
    print("The custom implementation matches Librosa's output!")
else:
    print("There is a significant difference between the two implementations.")
