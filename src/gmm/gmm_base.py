import pickle
from abc import ABC, abstractmethod

class GMMModelBase(ABC):
    """
    Abstract base class for the GMM model.

    Args:
        n_components (int): The number of Gaussian components to use in the GMM.
    """
    def __init__(self, n_components=16):
        """
        Initialize the GMM model.

        Args:
            n_components (int): The number of Gaussian components to use in the GMM.
        """
        self.n_components = n_components
        self.model = None  # Placeholder for the trained model

    @abstractmethod
    def train(self, data):
        """
        Train the model using data.

        This method should be overridden by subclasses of GMMModel and
        contain the code that should be run when the model is trained.

        Args:
            data (list or np.ndarray): The data to use for training.
        """

    def save(self, file_path):
        """Serialize and save the model."""
        with open(file_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, file_path):
        """
        Deserialize and load the model from a file.

        Args:
            file_path (str): The path to the file containing the serialized model.
        """
        with open(file_path, 'rb') as f:
            # Deserialize the model from the file
            self.model = pickle.load(f)
