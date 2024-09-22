from src.gmm.gmm_gaussian import GMMGaussianModel 

"""
GMM Factory Module

This module provides a factory class, GMMFactory, 
for creating Gaussian Mixture Model (GMM) instances. 
The factory class allows users to easily create GMM models 
with desired configuration parameters, such as the number of 
Gaussian components, covariance type, and maximum number of 
iterations for training the GMM.

The GMM model instances created by the factory class 
are instances of the GMMGaussianModel class, which is 
defined in the gmm_gaussian module.

The main purpose of this module is to provide a convenient 
way to create GMM models with desired configuration 
parameters. The factory class encapsulates the details 
of creating and configuring GMM models, and provides a 
simple interface for users to create GMM models with 
desired configuration parameters.

"""

class GMMFactory:
    def __init__(self, num_components=16, covariance_type='diag', max_iter=200):
        """
        Initialize the GMM Factory with desired configuration.
        
        Args:
            num_components (int): The number of Gaussian components in the model.
            covariance_type (str): Covariance type ('full', 'tied', 'diag', 'spherical').
            max_iter (int): Maximum number of iterations for training the GMM.
        """
        self.num_components = num_components
        self.covariance_type = covariance_type
        self.max_iter = max_iter

    def create_gmm_model(self):
        """
        Create a new GMM model with the current factory configuration.
        
        Returns:
            GMMGaussianModel: A new GMM model instance with the specified configuration.
        """
        return GMMGaussianModel(
            n_components=self.num_components, 
            covariance_type=self.covariance_type, 
            max_iter=self.max_iter
        )
