import numpy as np
import librosa
import matplotlib.pyplot as plt

class MelScaleFilterbank:
    def __init__(self, sample_rate, num_filters, fft_size, low_freq=0, high_freq=None):
        """
        Initialize the Mel-scale filterbank using Librosa.
        
        Args:
            sample_rate (int): The sampling rate of the audio signal.
            num_filters (int): The number of filters in the filterbank.
            fft_size (int): The size of the FFT (number of frequency bins).
            low_freq (float): The lowest frequency for the filterbank (default 0 Hz).
            high_freq (float): The highest frequency for the filterbank (default is Nyquist frequency).
        """
        self.sample_rate = sample_rate
        self.num_filters = num_filters
        self.fft_size = fft_size
        self.low_freq = low_freq
        self.high_freq = high_freq or sample_rate / 2
        
        # Generate the Mel filterbank using Librosa
        self.filterbank = librosa.filters.mel(
            sr=self.sample_rate,
            n_fft=self.fft_size,
            n_mels=self.num_filters,
            fmin=self.low_freq,
            fmax=self.high_freq
        )
        
    def apply(self, power_spectrum):
        """
        Apply the Mel-scale filterbank to the power spectrum.

        Args:
            power_spectrum (np.ndarray): The power spectrum of the frames (shape: [num_frames, fft_size // 2 + 1]).
        
        Returns:
            np.ndarray: The Mel-filtered spectrum.
        """
        return np.dot(self.filterbank, power_spectrum.T).T

# Test and visualize
if __name__ == "__main__":
    # Test signal parameters
    sample_rate = 16000  # 16 kHz
    fft_size = 512       # FFT size
    num_filters = 26     # Number of Mel filters
    
    # Create an example power spectrum (shape: [2 frames, fft_size // 2 + 1])
    power_spectrum = np.random.random((2, fft_size // 2 + 1))  # Example random power spectrum for 2 frames
    
    # Initialize Mel filterbank
    mel_filterbank = MelScaleFilterbank(
        sample_rate=sample_rate,
        num_filters=num_filters,
        fft_size=fft_size
    )
    
    # Apply the filterbank
    mel_spectrum = mel_filterbank.apply(power_spectrum)

    # Plot the filterbank
    plt.figure(figsize=(10, 6))
    for i in range(num_filters):
        plt.plot(mel_filterbank.filterbank[i], label=f'Filter {i + 1}')
    plt.title('Mel Filterbank (Triangular Filters)')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.savefig('mel_filterbank.png')  # Save as imag
    plt.close()  # Close the figure after saving
    plt.show()

    # Plot the power spectrum before applying the Mel filterbank
    plt.figure(figsize=(10, 4))
    plt.plot(power_spectrum[0], label='Original Power Spectrum (Frame 1)')
    plt.title('Original Power Spectrum (Frame 1)')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Power')
    plt.grid(True)
    plt.savefig('original_power_spectrum.png')  # Save as imag
    plt.close()  # Close the figure after saving
    plt.show()

    # Plot the Mel-filtered spectrum
    plt.figure(figsize=(10, 4))
    plt.plot(mel_spectrum[0], label='Mel-Filtered Spectrum (Frame 1)')
    plt.title('Mel-Filtered Spectrum (Frame 1)')
    plt.xlabel('Filter Index')
    plt.ylabel('Power')
    plt.grid(True)
    plt.savefig('mel_filtered_spectrum.png')  # Save as image
    plt.close()  # Close the figure after saving
    plt.show()
 