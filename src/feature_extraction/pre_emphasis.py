# This module responsible for applying the pre-emphasis filter to the input signal.

#Pre-Emphasis Filter:
#The pre-emphasis filter emphasizes higher frequencies in the audio signal. 
#It is a high-pass filter applied to the signal to balance the frequency spectrum and 
#make it easier to extract relevant features.
# The equation for the pre-emphasis filter is as follows:
# y[t]=x[t]−αx[t−1]
#Where:
#y[t] is the output signal.
#x[t] is the input signal.
#α is the pre-emphasis coefficient, usually between 0.95 and 0.99.
class PreEmphasisFilter:
    """
    Class to apply a pre-emphasis filter to an input audio signal.

    Attributes:
        alpha (float): Pre-emphasis coefficient, typically between 0.95 and 0.99.
    """

    def __init__(self, alpha=0.97):
        """
        Initialize the PreEmphasisFilter filter with a specific alpha value.
        
        Args:
            alpha (float): The pre-emphasis coefficient. Defaults to 0.97.
        """
        self.alpha = alpha

    def apply_filter(self, signal):
        """
        Apply the pre-emphasis filter to the input signal.
        
        Args:
            signal (list or numpy array): The input audio signal.
        
        Returns:
            list: The pre-emphasized signal.
        """
        # Initialize the output signal array with the same length as the input
        emphasized_signal = [signal[0]]  # First element remains the same
        
        # Apply the filter to each sample in the signal
        for i in range(1, len(signal)):
            emphasized_signal.append(signal[i] - self.alpha * signal[i - 1])

        return emphasized_signal

if __name__ == "__main__":
    # Example signal
    input_signal = [0.1, 0.2, 0.4, 0.5, 0.3, 0.2]

    # Initialize the PreEmphasisFilter filter with a default alpha
    pre_emphasis = PreEmphasisFilter(alpha=0.97)
    
    # Apply the filter
    output_signal = pre_emphasis.apply_filter(input_signal)

    # Print the result
    print(f"Input signal: {input_signal}")
    print(f"Pre-emphasized signal: {output_signal}")
