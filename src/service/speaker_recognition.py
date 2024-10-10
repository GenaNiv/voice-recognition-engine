# speaker_recognition.py
import os
import hashlib
from speaker_enrollment import AudioFeatureExtractor
from gmm.gmm_factory import GMMFactory
from file_management.file_management import FileManagementInterface

class SpeakerRecognition:
    def __init__(self, bst, base_directory, sample_rate, frame_size, frame_step, fft_size, num_filters, num_ceps):
        """
        Initialize a new SpeakerRecognition object.
        
        Args:
            file_manager: An instance responsible for managing file operations.
            gmm_factory: An instance responsible for creating GMM models.
        """
        self.audio_extractor = AudioFeatureExtractor(sample_rate=sample_rate, frame_size=frame_size, frame_step=frame_step, fft_size=fft_size, num_filters=num_filters, num_ceps=num_ceps)
        self.file_manager = FileManagementInterface(bst=bst, base_directory=base_directory)  
        self.gmm_factory = GMMFactory()

    def recognize_speaker(self, wav_file_path):
        """
        Recognize a speaker by comparing the input audio file with enrolled GMM models.
        
        Args:
            wav_file_path (str): Path to the audio file (.wav) of the speaker to recognize.
        
        Returns:
            str: The name or ID of the recognized speaker, or None if no match is found.
        """
        # Step 1: Extract MFCC features from the audio file
        try:
            signal = self.audio_extractor.load_wav(wav_file_path)
            mfcc_features = self.audio_extractor.extract_features(signal)
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return None

        # Step 2: Load enrolled GMM models and compute likelihoods
        try:
            model_directory = "models/"
            best_score = float('-inf')
            recognized_speaker = None
            
            # Iterate over each GMM model stored in the models directory
            for model_file in os.listdir(os.path.join(self.file_manager.base_directory, model_directory)):
                model_path = os.path.join(model_directory, model_file)

                # Generate the file ID from the model path
                file_id = hashlib.md5(model_path.encode()).hexdigest()
                
                # Load the GMM model using the file_id
                serialized_model = self.file_manager.get_file_content(file_id)
                
                if serialized_model is None:
                    continue  # Skip this model if it couldn't be loaded

                # Deserialize the GMM model
                gmm_model = self.gmm_factory.create_gmm_model()
                gmm_model.deserialize_model(serialized_model)

                # Step 3: Calculate likelihood score for the extracted MFCC features
                score = gmm_model.model.score(mfcc_features)  # Using GaussianMixture's score() method
                
                # Compare scores to find the best match
                if score > best_score:
                    best_score = score
                    recognized_speaker = model_file.split("_gmm_model.pkl")[0]  # Extract speaker name from the file name

        except Exception as e:
            print(f"Error loading GMM models: {e}")
            return None

        # Step 4: Return the recognized speaker or None if no match is found
        if recognized_speaker:
            print(f"Recognized speaker: {recognized_speaker}")
            return recognized_speaker
        else:
            print("No matching speaker found.")
            return None