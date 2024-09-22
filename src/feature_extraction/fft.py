import numpy as np

class FFTProcessor:
    def __init__(self, n_fft):
        """
        Initialize the FFT processor.

        This class is responsible for computing the Fast Fourier Transform (FFT) of the input signal
        and calculating the power spectrum.

        Args:
            n_fft (int): The number of FFT points to compute (typically the frame length or next power of 2).
                         This parameter determines the resolution of the frequency domain representation.
                         Larger values will result in a higher frequency resolution, but will also increase
                         the computational cost of the FFT.
        """
        self.n_fft = n_fft

    def compute_fft(self, frames):
        """
        Compute the FFT for each frame.

        Args:
            frames (np.ndarray): 2D array where each row is a frame.
        
        Returns:
            np.ndarray: The FFT result of the frames.
        """
        # Apply FFT to each frame
        fft_result = np.fft.rfft(frames, n=self.n_fft)
        return fft_result

    def compute_power_spectrum(self, fft_result):
        """
        Compute the power spectrum from the FFT result.

        Args:
            fft_result (np.ndarray): FFT output for each frame (complex numbers).
        
        Returns:
            np.ndarray: Power spectrum (|FFT|^2) of the frames.
        """
        # Compute the power spectrum (|FFT|^2)
        power_spectrum = np.abs(fft_result) ** 2
        return power_spectrum
    
if __name__ == "__main__":
    # Example usage

    # Example signal (2D array with rows representing frames)
    frames = np.array([[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]])

    # Initialize FFT processor
    fft_processor = FFTProcessor(n_fft=4)

    # Compute FFT
    fft_result = fft_processor.compute_fft(frames)

    # Compute Power Spectrum
    power_spectrum = fft_processor.compute_power_spectrum(fft_result)

    print("FFT Result:", fft_result)
    print("Power Spectrum:", power_spectrum)
