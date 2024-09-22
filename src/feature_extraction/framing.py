#In this step, the continuous speech signal is divided into small, overlapping segments called frames. 
#The idea is to capture short-term stationary characteristics of the speech signal, 
#as speech is non-stationary over time but can be considered stationary for short periods.

#Key Concepts:
#Frame Size: Typically 20-40 milliseconds (ms) in length. A common value is 25ms.
#Frame Step (Overlap): Typically the frames overlap by 10-15ms to ensure the continuity of features 
#from one frame to the next.
#Purpose: Framing breaks the continuous signal into chunks that are easier to process and analyze. 
#Each frame will later undergo further feature extraction, like applying the Fast Fourier Transform (FFT) or 
#Mel Filterbank.

import numpy as np

class Framing:
    def __init__(self, frame_size, frame_step, sample_rate):
        """
        Initialize the Framing class.

        Args:
            frame_size (float): Frame size in seconds.
            frame_step (float): Frame step (overlap) in seconds.
            sample_rate (int): The sampling rate of the audio signal.
        """
        self.frame_size = frame_size
        self.frame_step = frame_step
        self.sample_rate = sample_rate

    def frame_signal(self, signal):
        """
        Frame the given signal into overlapping frames.

        Args:
            signal (list): The input audio signal.

        Returns:
            2D list: A list of frames, where each frame is a sub-list of signal samples.
        """
        # Convert frame size and step from seconds to samples
        frame_length = int(self.frame_size * self.sample_rate)
        frame_step = int(self.frame_step * self.sample_rate)

        # Calculate the total number of frames
        signal_length = len(signal)
        num_frames = int(np.ceil(float(signal_length - frame_length) / frame_step)) + 1

        # Pad the signal if necessary to ensure we get all frames
        pad_signal_length = num_frames * frame_step + frame_length
        padding = np.zeros((pad_signal_length - signal_length,))
        padded_signal = np.concatenate((signal, padding))

        # Generate the frames
        frames = []
        for i in range(0, num_frames):
            # Calculate the start index of the current frame
            start_index = i * frame_step

            # Extract the current frame from the padded signal
            frame = padded_signal[start_index:start_index + frame_length]

            # Append the current frame to the frames list
            frames.append(frame)
        
        # Convert the frames list to a numpy array
        return np.array(frames)

if __name__ == "__main__":
    # Example usage:
    # Example signal (just for testing)
    test_signal = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Frame size and step (in seconds)
    frame_size = 0.05  # 50 ms
    frame_step = 0.02  # 20 ms
    sample_rate = 100  # 100 samples per second

    # Initialize Framing class
    framing = Framing(frame_size, frame_step, sample_rate)

    # Frame the signal
    frames = framing.frame_signal(test_signal)

    # Print the results
    print(f"Original signal: {test_signal}")
    print(f"Number of frames: {len(frames)}")
    print(f"Frames:\n{frames}")