# gmm_gaussian.py
from sklearn.mixture import GaussianMixture
import pickle

from src.gmm.gmm_base import GMMModelBase

class GMMGaussianModel(GMMModelBase):
    """
    A Gaussian Mixture Model (GMM) that uses Gaussian distributions
    as the components.

    Parameters
    ----------
    n_components : int, optional
        The number of components in the GMM. Defaults to 16.
    covariance_type : str, optional
        The type of covariance matrix to use. Can be either
        'full' or 'diag'. Defaults to 'diag'.
    max_iter : int, optional
        The maximum number of iterations to run the Expectation-Maximization algorithm. Defaults to 100.
    """

    def __init__(self, n_components=16, covariance_type='diag', max_iter=100):
        """
        Initialize the GMM.
        """
        super().__init__(n_components=n_components)
        self.covariance_type = covariance_type
        self.max_iter = max_iter
        self.model = None  # Will hold the trained GMM model

    def train(self, data):
        """
        Train the GMM using Expectation-Maximization.

        Parameters
        ----------
        data : array-like, shape (n_samples, n_features)
            The data to use to train the GMM.
        """
        # Initialize the GMM model
        self.model = GaussianMixture(
            n_components=self.n_components, 
            covariance_type=self.covariance_type,
            max_iter=self.max_iter)

        # Train the GMM using Expectation-Maximization
        self.model.fit(data)
        print("Model training complete.")

    def serialize_model(self):
        """
        Serialize the trained GMM model and return it.

        Returns
        -------
        bytes
            The serialized GMM model.
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        
        # Serialize the model using pickle
        serialized_model = pickle.dumps(self.model)
        print("Model serialized successfully using pickle.")
        return serialized_model


    def deserialize_model(self, serialized_model):
        """
        Deserialize the provided model and load it into the instance.

        Parameters
        ----------
        serialized_model : bytes
            The serialized GMM model.
        """
        self.model = pickle.loads(serialized_model)
        print("Model deserialized successfully using pickle.")

    def predict(self, data):
        """
        Use the trained GMM model to predict the labels for data.

        Parameters
        ----------
        data : array-like, shape (n_samples, n_features)
            The data to predict labels for.

        Returns
        -------
        labels : array, shape (n_samples,)
            Component labels for each sample.
        """
        if self.model is None:
            raise ValueError("Model has not been trained or loaded.")
        
        return self.model.predict(data)