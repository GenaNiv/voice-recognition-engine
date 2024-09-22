import numpy as np
import matplotlib.pyplot as plt
import librosa
from src.feature_extraction.pre_emphasis import PreEmphasisFilter
from src.feature_extraction.framing import Framing
from src.feature_extraction.hamming_window import HammingWindow
from src.feature_extraction.fft import FFTProcessor
from src.feature_extraction.mel_filterbank import MelScaleFilterbank
from src.feature_extraction.dct_processor import DCTProcessor, LogarithmCompression

class AudioFeatureExtractor:
    def __init__(self, sample_rate=16000, frame_size=0.025, frame_step=0.01, fft_size=512, num_filters=26, num_ceps=13):
        """
        Initialize the feature extractor with default parameters for MFCC feature extraction.

        Args:
            sample_rate (int): The sampling rate of the audio signal.
            frame_size (float): Frame size in seconds.
            frame_step (float): Frame step (overlap) in seconds.
            fft_size (int): The size of the FFT (number of frequency bins).
            num_filters (int): The number of filters in the Mel filterbank.
            num_ceps (int): The number of MFCC coefficients to retain.
        """
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.frame_step = frame_step
        self.fft_size = fft_size
        self.num_filters = num_filters
        self.num_ceps = num_ceps

        # Initialize all processing components
        self.pre_emphasis_filter = PreEmphasisFilter()
        self.framing = Framing(self.frame_size, self.frame_step, self.sample_rate)
        self.hamming_window = HammingWindow(int(self.frame_size * self.sample_rate))
        self.fft_processor = FFTProcessor(self.fft_size)
        self.mel_filterbank = MelScaleFilterbank(self.sample_rate, self.num_filters, self.fft_size)
        self.dct_processor = DCTProcessor(self.num_ceps)
        self.log_compressor = LogarithmCompression()

    def extract_features(self, signal):
        """
        Extract MFCC features from a given audio signal.

        Args:
            signal (np.ndarray): The raw audio signal.
        Returns:
            np.ndarray: The MFCC features extracted from the audio signal.
        """
        # Step 1: Apply pre-emphasis filter
        pre_emphasized_signal = self.pre_emphasis_filter.apply_filter(signal)
        
        # Step 2: Frame the signal
        frames = self.framing.frame_signal(pre_emphasized_signal)
        
        # Step 3: Apply Hamming window
        windowed_frames = self.hamming_window.apply(frames)
        
        # Step 4: Compute FFT
        fft_result = self.fft_processor.compute_fft(windowed_frames)
        
        # Step 5: Compute power spectrum
        power_spectrum = self.fft_processor.compute_power_spectrum(fft_result)
        
        # Step 6: Apply Mel filterbank
        mel_spectrum = self.mel_filterbank.apply(power_spectrum)
        
        # Step 7: Apply logarithm compression
        log_mel_spectrum = self.log_compressor.apply(mel_spectrum)
        
        # Step 8: Compute MFCCs using DCT
        mfcc_features = self.dct_processor.compute_dct(log_mel_spectrum)
        #test
        print(type(mfcc_features))
        if isinstance(mfcc_features, np.ndarray):
            print("mfcc_features is a numpy array.")
        else:
            print("mfcc_features is not a numpy array.")
        
        return mfcc_features

    def load_wav(self, filepath):
        """
        Load a .wav file and return its signal.

        Args:
            filepath (str): The path to the .wav file.

        Returns:
            np.ndarray: The loaded audio signal.
        """
        signal, _ = librosa.load(filepath, sr=self.sample_rate)
        return signal
def visualize_mfcc(mfcc_features, sample_rate, hop_length):
    """
    Visualize MFCC features using a heatmap.

    Args:
        mfcc_features (np.ndarray): The extracted MFCC features (2D array: frames x coefficients).
        sample_rate (int): The sample rate of the audio signal.
        hop_length (int): The number of samples between successive frames (used to calculate time axis).
    """
    # Create time axis in seconds
    num_frames = mfcc_features.shape[0]
    time_axis = np.arange(num_frames) * hop_length / sample_rate
    
    # Plot heatmap of MFCCs
    plt.figure(figsize=(10, 6))
    plt.imshow(mfcc_features.T, aspect='auto', origin='lower', cmap='jet', extent=[time_axis.min(), time_axis.max(), 0, mfcc_features.shape[1]])
    plt.colorbar(format='%+2.0f dB')
    plt.title('MFCC Features')
    plt.xlabel('Time (s)')
    plt.ylabel('MFCC Coefficients')
    plt.tight_layout()
    plt.show()
    # Save the image as a file
    plt.savefig("custome_mfcc.png")
    plt.close()  # Close the figure after saving
    
def plot_mfcc_coefficients_over_time(mfcc_features, sample_rate, hop_length):
    # Only keep the first 13 coefficients
    mfcc_features = mfcc_features[:13, :]  # Keep the first 13 coefficients

    # Time axis for the x-axis
    time_axis = np.arange(mfcc_features.shape[1]) * hop_length / sample_rate

    plt.figure(figsize=(10, 6))
    
    # Plot each coefficient over time
    for i in range(mfcc_features.shape[0]):
        plt.plot(time_axis, mfcc_features[i, :], label=f'Coefficient {i+1}')
    
    plt.title('MFCC Coefficients Over Time (First 13 Coefficients)')
    plt.xlabel('Time (s)')
    plt.ylabel('Coefficient Value')
    plt.legend(loc='upper right')  # Adjust legend position if needed
    plt.grid(True)
    plt.savefig('mfcc_over_time_13coeff.png')  # Save the plot as an image
    plt.show()
    
# Example usage
if __name__ == "__main__":
    extractor = AudioFeatureExtractor()

    # Load a test wav file (replace 'path_to_wav' with your actual file path)
    signal = extractor.load_wav('gena.wav')

    # Extract MFCC features
    mfcc_features = extractor.extract_features(signal)

    print("MFCC Features:")
    print(mfcc_features)
    
    sample_rate = 16000  # Example sample rate in Hz
    hop_length = 512     # Example hop length in samples

    visualize_mfcc(mfcc_features, sample_rate, hop_length)
    
    
    librosa_mfcc = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=13, hop_length=hop_length)
    
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa_mfcc, sr=sample_rate, hop_length=hop_length, x_axis='time')
    plt.colorbar()
    plt.title('Librosa MFCC')
    plt.xlabel('Time')
    plt.ylabel('MFCC Coefficients')
    plt.savefig('librosa_mfcc.png')  # Save the librosa MFCC plot as an image
    plt.show()


    # Assuming you have extracted MFCC features
    # Replace with your MFCC features, sample rate, and hop length
    plot_mfcc_coefficients_over_time(mfcc_features, sample_rate=16000, hop_length=512)