#  Design of the Hamming Window
#  The Hamming window is a type of windowing function that reduces spectral leakage by tapering the edges 
#  of each frame before applying the FFT. The mathematical formula for the Hamming window is as follows:
#  w(n)=0.54-0.46cos(2πn/(N-1))
#
#  Where:
#  
#  w(n) is the Hamming window value for sample 
#  N is the total number of samples in the window (frame size).
#  n ranges from 0 to N - 1
#  Purpose: The Hamming window reduces discontinuities at the edges of the frame, 
#  which would otherwise create artifacts in the frequency domain after applying FFT.
#  
#  Key Points of Implementation:
#  The window should be computed for each frame, based on the frame size.
#  The window is element-wise multiplied with each frame before the FFT step.

import numpy as np

import numpy as np

class HammingWindow:
    def __init__(self, frame_length):
        """
        Initialize the HammingWindow class.

        The Hamming window is a type of windowing function that reduces spectral leakage by tapering the edges 
        of each frame before applying the FFT. The mathematical formula for the Hamming window is as follows:
        w(n)=0.54-0.46cos(2πn/(N-1))

        Where:

        w(n) is the Hamming window value for sample 
        N is the total number of samples in the window (frame size).
        n ranges from 0 to N - 1

        Purpose: The Hamming window reduces discontinuities at the edges of the frame, 
        which would otherwise create artifacts in the frequency domain after applying FFT.

        Key Points of Implementation:
        The window should be computed for each frame, based on the frame size.
        The window is element-wise multiplied with each frame before the FFT step.

        Args:
            frame_length (int): The length of each frame.
        """
        self.frame_length = frame_length
        self.hamming_window = self._compute_hamming_window()

    def _compute_hamming_window(self):
        """
        Compute the Hamming window for a given frame length.
        
        Returns:
            np.ndarray: The Hamming window of the same length as the frame.
        """
        return 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(self.frame_length) / (self.frame_length - 1))

    def apply(self, frames):
        """
        Apply the Hamming window to each frame in the input signal.
        
        Args:
            frames (np.ndarray): 2D array where each row is a frame.
            
        Returns:
            np.ndarray: The windowed frames.
        """
        return frames * self.hamming_window
