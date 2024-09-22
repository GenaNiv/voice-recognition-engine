import numpy as np
from scipy.fftpack import dct

class DCTProcessor:
    def __init__(self, num_ceps):
        """
        Initialize the DCT processor for computing MFCCs.

        Args:
            num_ceps (int): The number of MFCC coefficients to retain.
        """
        self.num_ceps = num_ceps

    def compute_dct(self, log_mel_spectrum):
        """
        Compute the Discrete Cosine Transform (DCT) on the log Mel-filtered spectrum to get MFCCs.

        Args:
            log_mel_spectrum (np.ndarray): The log-compressed Mel-filtered spectrum.
        
        Returns:
            np.ndarray: The MFCCs for the input Mel-filtered spectrum.
        """
        # Apply the DCT to each frame's log Mel-filtered spectrum and keep the first num_ceps coefficients
        mfcc = dct(log_mel_spectrum, type=2, axis=1, norm='ortho')[:, :self.num_ceps]
        print(f"The shape of MFCC is {mfcc.shape}")
        return mfcc

class LogarithmCompression:
    def __init__(self, epsilon=1e-10):
        """
        Initialize the LogarithmCompression class.

        Args:
            epsilon (float): A small value to prevent taking the logarithm of zero.
        """
        self.epsilon = epsilon
    
    def apply(self, mel_spectrum):
        """
        Apply logarithmic compression to the Mel-filtered spectrum.
        
        Args:
            mel_spectrum (np.ndarray): The Mel-filtered spectrum.
        
        Returns:
            np.ndarray: The log-compressed Mel spectrum.
        """
        return np.log(mel_spectrum + self.epsilon)

# Example Testing
if __name__ == "__main__":
    # Example Mel-filtered spectrum (2 frames for testing)
    mel_spectrum = np.array([
        [0.1, 0.2, 0.3, 0.4],  # Example frame 1
        [0.2, 0.3, 0.4, 0.5]   # Example frame 2
    ])

    # Apply logarithmic compression
    log_compressor = LogarithmCompression()
    log_mel_spectrum = log_compressor.apply(mel_spectrum)
    print("Log-compressed Mel Spectrum:")
    print(log_mel_spectrum)

    # Initialize DCT processor
    num_ceps = 13  # Number of MFCC coefficients to retain
    dct_processor = DCTProcessor(num_ceps=num_ceps)

    # Compute MFCCs
    mfcc_result = dct_processor.compute_dct(log_mel_spectrum)

    print("\nMFCC Result:")
    print(mfcc_result)
