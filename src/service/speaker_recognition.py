# speaker_recognition.py
import hashlib
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

from feature_extraction.audio_feature_extractor import AudioFeatureExtractor
from file_management.file_management import FileManagementInterface
from gmm.gmm_factory import GMMFactory


@dataclass
class RecognitionComputation:
    """Container for low-level recognition results."""

    speaker: Optional[str]
    best_score: float
    scores: List[Tuple[str, float]]
    rejected: bool = False


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

    def recognize_speaker(self, wav_file_path, score_threshold=None):
        """
        Process a wav file, run recognition, and return the matched speaker.

        This method remains compatible with the CLI by accepting a filesystem
        path, but under the hood it delegates most of the work to
        `recognize_signal`, which enables the new in-memory workflows exposed
        via the service API.
        """
        # Step 1: Extract MFCC features from the audio file
        try:
            signal = self.audio_extractor.load_wav(wav_file_path)
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return None

        result = self.recognize_signal(signal, score_threshold=score_threshold)
        if result is None:
            return None

        if result.scores:
            print("Likelihood scores (higher is better):")
            for name, score in sorted(result.scores, key=lambda item: item[1], reverse=True):
                print(f"  {name}: {score:.4f}")
            if result.best_score != float("-inf"):
                print(f"Best score: {result.best_score:.4f}")
            if score_threshold is not None:
                margin = result.best_score - score_threshold
                print(f"Score threshold: {score_threshold:.4f} (margin {margin:.4f})")

        if not result.speaker:
            print("No matching speaker found.")
            return None

        if result.rejected:
            print("Best score did not meet threshold; rejecting match.")
            return None

        print(f"Recognized speaker: {result.speaker}")
        return result.speaker

    def recognize_signal(self, signal, score_threshold=None):
        """
        Recognize a speaker directly from an audio signal.

        Args:
            signal (numpy.ndarray): Raw PCM samples.
            score_threshold (float, optional): Minimum acceptable likelihood.

        Returns:
            RecognitionComputation or None if processing fails.
        """
        try:
            mfcc_features = self.audio_extractor.extract_features(signal)
        except Exception as e:
            print(f"Error processing audio signal: {e}")
            return None

        return self._evaluate_scores(mfcc_features, score_threshold)

    def _evaluate_scores(self, mfcc_features, score_threshold=None):
        """
        Compute recognition scores across enrolled GMM models.

        Args:
            mfcc_features (numpy.ndarray): Extracted MFCC feature set.
            score_threshold (float, optional): Minimum acceptable likelihood.

        Returns:
            RecognitionComputation: Structured result containing scores.
        """
        try:
            recognized_speaker, best_score, speaker_scores = self._score_models(mfcc_features)
        except Exception as e:
            print(f"Error loading GMM models: {e}")
            return None

        if not speaker_scores:
            return RecognitionComputation(speaker=None, best_score=float("-inf"), scores=[], rejected=True)

        rejected = score_threshold is not None and best_score < score_threshold
        return RecognitionComputation(
            speaker=recognized_speaker,
            best_score=best_score,
            scores=speaker_scores,
            rejected=rejected
        )

    def _score_models(self, mfcc_features):
        """
        Iterate through enrolled models and compute likelihood scores.

        Returns:
            tuple[str | None, float, list[tuple[str, float]]]
        """
        model_directory = "models/"
        best_score = float('-inf')
        recognized_speaker = None
        speaker_scores: List[Tuple[str, float]] = []

        models_base = os.path.join(self.file_manager.base_directory, model_directory)
        if not os.path.exists(models_base):
            return recognized_speaker, best_score, speaker_scores

        for model_file in os.listdir(models_base):
            model_path = os.path.join(model_directory, model_file)
            file_id = hashlib.md5(model_path.encode()).hexdigest()
            serialized_model = self.file_manager.get_file_content(file_id)

            if serialized_model is None:
                continue

            gmm_model = self.gmm_factory.create_gmm_model()
            gmm_model.deserialize_model(serialized_model)

            score = gmm_model.model.score(mfcc_features)
            speaker_name = model_file.split("_gmm_model.pkl")[0]
            speaker_scores.append((speaker_name, score))

            if score > best_score:
                best_score = score
                recognized_speaker = speaker_name

        return recognized_speaker, best_score, speaker_scores
