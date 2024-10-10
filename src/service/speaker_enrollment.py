import os
from feature_extraction.audio_feature_extractor import AudioFeatureExtractor
from gmm.gmm_factory import GMMFactory
from file_management.file_management import FileManagementInterface

class SpeakerEnrollment:
    def __init__(
        self, 
        bst, 
        base_directory, 
        sample_rate=16000, 
        num_filters=26, 
        num_ceps=13, 
        n_fft=512, 
        frame_size=0.025, 
        frame_step=0.01, 
        n_mixtures=8
    ):
        """
        Initialize SpeakerEnrollment with necessary parameters.
        
        Args:
            bst (BinarySearchTree): The binary search tree for managing metadata.
            base_directory (str): The base directory where the GMM models will be saved.
            sample_rate (int): Sample rate of audio files.
            num_filters (int): Number of Mel filters.
            num_ceps (int): Number of MFCC coefficients.
            n_fft (int): FFT size for audio processing.
            frame_size (float): Frame size in seconds.
            frame_step (float): Frame step (overlap) in seconds.
            n_mixtures (int): Number of Gaussian mixtures in GMM.
        """
        self.audio_extractor = AudioFeatureExtractor(
            sample_rate=sample_rate,
            frame_size=frame_size,
            frame_step=frame_step,
            fft_size=n_fft,
            num_filters=num_filters,
            num_ceps=num_ceps
        )
        self.gmm_factory = GMMFactory(num_components=n_mixtures)
        self.file_manager = FileManagementInterface(bst, base_directory)

    def enroll_speaker(self, speaker_name, wav_file_path):
        """
        Enroll a speaker by extracting MFCCs and training a GMM model.
        
        Args:
            speaker_name (str): The name or ID of the speaker to enroll.
            wav_file_path (str): Path to the speaker's audio file (.wav).
        
        Returns:
            bool: Returns True if enrollment is successful, False otherwise.
        """
        try:
            # Step 1: Extract MFCC features from the audio file
            signal = self.audio_extractor.load_wav(wav_file_path)
            mfcc_features = self.audio_extractor.extract_features(signal)

            # Step 2: Train a GMM model using the extracted MFCC features
            gmm_model = self.gmm_factory.create_gmm_model()
            gmm_model.train(mfcc_features)

            # Step 3: Save the GMM model using the file management system
            # Create the relative path to save the model under "models" folder
            model_filename = f"{speaker_name}_gmm_model.pkl"
            model_file_path = os.path.join("models", model_filename)  # Relative path

            # Serialize and save the GMM model
            self.file_manager.add_file(model_file_path, gmm_model.serialize_model())

            # Step 4: Save speaker metadata as well
            file_content = f"Speaker: {speaker_name}\nGMM Model Path: {model_file_path}"
            metadata_filename = f"{speaker_name}_metadata.txt"
            metadata_file_path = os.path.join("metadata", metadata_filename)

            self.file_manager.add_file(metadata_file_path, file_content)

            print(f"Speaker '{speaker_name}' enrolled successfully.")
            return True

        except Exception as e:
            print(f"Error enrolling speaker: {e}")
            return False
