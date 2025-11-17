# src/service/api.py
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Protocol

import numpy as np

from file_management.bst import BinarySearchTree
from file_management.file_management import FileManagementInterface
from service.speaker_enrollment import SpeakerEnrollment
from service.speaker_recognition import RecognitionComputation, SpeakerRecognition


@dataclass(frozen=True)
class EnrollmentConfig:
    """Configuration object for enrollment requests."""

    sample_rate: int = 16000
    num_filters: int = 26
    num_ceps: int = 13
    fft_size: int = 512
    frame_size: float = 0.025
    frame_step: float = 0.01
    mixtures: int = 8


@dataclass(frozen=True)
class RecognitionConfig:
    """Configuration object for recognition requests."""

    sample_rate: int = 16000
    frame_size: float = 0.025
    frame_step: float = 0.01
    fft_size: int = 512
    num_filters: int = 26
    num_ceps: int = 13


class AudioSource(Protocol):
    """Protocol describing an audio input provider."""

    def stream(self) -> Iterable[np.ndarray]:
        """Yield successive PCM frames that upstream code can consume."""


class StreamingRecognitionSession(Protocol):
    """Incremental recognition contract for live audio."""

    def consume(self, frame: np.ndarray) -> Optional["RecognitionResult"]:
        """
        Feed the next PCM frame into the running recognition pipeline.

        Returns:
            RecognitionResult or None: Updated recognition output if enough
            context has been processed, otherwise None.
        """

    def close(self) -> None:
        """
        Release buffered resources and finalize the recognition session.

        Implementations should flush pending frames and persist any state.
        """


@dataclass
class SpeakerSummary:
    speaker_id: str
    metadata_path: str


@dataclass
class EnrollmentRequest:
    speaker_id: str
    audio_source: AudioSource
    config: EnrollmentConfig = field(default_factory=EnrollmentConfig)


@dataclass
class EnrollmentResult:
    speaker_id: str
    model_path: str
    metadata_path: str


@dataclass
class RecognitionRequest:
    audio_source: AudioSource
    threshold: Optional[float] = None
    config: RecognitionConfig = field(default_factory=RecognitionConfig)


@dataclass
class RecognitionResult:
    speaker_id: Optional[str]
    score: float
    scores: dict[str, float]
    rejected: bool = False


class VoiceRecognitionService:
    """High-level façade for enrollment and recognition workflows."""

    def __init__(self, bst: BinarySearchTree, base_directory: str):
        self._bst = bst
        self._base_directory = base_directory
        self._file_manager = FileManagementInterface(self._bst, self._base_directory)
        self._enrollment_cache: dict[EnrollmentConfig, SpeakerEnrollment] = {}
        self._recognition_cache: dict[RecognitionConfig, SpeakerRecognition] = {}

    def enroll(self, req: EnrollmentRequest) -> EnrollmentResult:
        """Enroll a new speaker and return paths to persisted assets."""
        signal = self._collect_signal(req.audio_source)
        enrollment = self._get_enrollment(req.config)
        model_path, metadata_path = enrollment.enroll_from_signal(req.speaker_id, signal)
        return EnrollmentResult(
            speaker_id=req.speaker_id,
            model_path=self._resolve_path(model_path),
            metadata_path=self._resolve_path(metadata_path),
        )

    def recognize(self, req: RecognitionRequest) -> RecognitionResult:
        """Run recognition on the supplied audio source and return scores."""
        signal = self._collect_signal(req.audio_source)
        return self._recognize_signal(signal, req.config, req.threshold)

    def list_speakers(self) -> list[SpeakerSummary]:
        """Return summaries for all speakers stored in the repository."""
        entries = self._file_manager.list_all_files() or []
        summaries: List[SpeakerSummary] = []

        for entry in entries:
            path = entry.get("file_path")
            if not path:
                continue
            filename = os.path.basename(path)
            if not filename.endswith("_metadata.txt"):
                continue
            speaker_id = filename.replace("_metadata.txt", "")
            summaries.append(SpeakerSummary(speaker_id=speaker_id, metadata_path=path))

        return summaries

    def delete_speaker(self, speaker_id: str) -> None:
        """Remove a speaker and associated assets from storage."""
        targets = [
            os.path.join("models", f"{speaker_id}_gmm_model.pkl"),
            os.path.join("metadata", f"{speaker_id}_metadata.txt"),
        ]
        for relative_path in targets:
            file_id = hashlib.md5(relative_path.encode()).hexdigest()
            try:
                self._file_manager.delete_file(file_id)
            except FileNotFoundError:
                continue

    def start_session(self, config: Optional[RecognitionConfig] = None, threshold: Optional[float] = None) -> StreamingRecognitionSession:
        """
        Start a streaming session capable of consuming live audio frames.

        Args:
            config: Recognition configuration overrides for the session.
            threshold: Optional minimum likelihood score for acceptance.
        """
        return _BufferingRecognitionSession(self, config or RecognitionConfig(), threshold)

    def _collect_signal(self, audio_source: AudioSource) -> np.ndarray:
        """Concatenate PCM frames from the provided audio source."""
        chunks: List[np.ndarray] = []
        for chunk in audio_source.stream():
            array = np.asarray(chunk)
            if array.size == 0:
                continue
            chunks.append(array)

        if not chunks:
            raise ValueError("Audio source produced no samples.")

        return np.concatenate(chunks)

    def _get_enrollment(self, config: EnrollmentConfig) -> SpeakerEnrollment:
        """Create or reuse a SpeakerEnrollment instance with the supplied config."""
        enrollment = self._enrollment_cache.get(config)
        if enrollment is not None:
            return enrollment

        enrollment = SpeakerEnrollment(
            bst=self._bst,
            base_directory=self._base_directory,
            sample_rate=config.sample_rate,
            num_filters=config.num_filters,
            num_ceps=config.num_ceps,
            n_fft=config.fft_size,
            frame_size=config.frame_size,
            frame_step=config.frame_step,
            n_mixtures=config.mixtures,
        )
        self._enrollment_cache[config] = enrollment
        return enrollment

    def _get_recognition(self, config: RecognitionConfig) -> SpeakerRecognition:
        """Create or reuse a SpeakerRecognition instance with the supplied config."""
        recognizer = self._recognition_cache.get(config)
        if recognizer is not None:
            return recognizer

        recognizer = SpeakerRecognition(
            bst=self._bst,
            base_directory=self._base_directory,
            sample_rate=config.sample_rate,
            frame_size=config.frame_size,
            frame_step=config.frame_step,
            fft_size=config.fft_size,
            num_filters=config.num_filters,
            num_ceps=config.num_ceps,
        )
        self._recognition_cache[config] = recognizer
        return recognizer

    def _recognize_signal(self, signal: np.ndarray, config: RecognitionConfig, threshold: Optional[float]) -> RecognitionResult:
        """Recognize from in-memory signal and convert to a service-level result."""
        recognition = self._get_recognition(config)
        outcome = recognition.recognize_signal(signal, score_threshold=threshold)

        if outcome is None or not outcome.scores:
            return RecognitionResult(speaker_id=None, score=float("-inf"), scores={}, rejected=True)

        scores = {name: score for name, score in outcome.scores}
        speaker_id = None if outcome.rejected else outcome.speaker

        return RecognitionResult(
            speaker_id=speaker_id,
            score=outcome.best_score,
            scores=scores,
            rejected=outcome.rejected or outcome.speaker is None,
        )

    def _resolve_path(self, relative_path: str) -> str:
        """Convert a relative storage path to an absolute location."""
        return os.path.join(self._base_directory, relative_path)


class _BufferingRecognitionSession(StreamingRecognitionSession):
    """Basic session that buffers frames and reruns recognition."""

    def __init__(self, service: VoiceRecognitionService, config: RecognitionConfig, threshold: Optional[float]):
        self._service = service
        self._config = config
        self._threshold = threshold
        self._frames: List[np.ndarray] = []
        self._min_samples = int(self._config.sample_rate * self._config.frame_size)

    def consume(self, frame: np.ndarray) -> Optional[RecognitionResult]:
        """
        Feed the next PCM frame into the running recognition pipeline.

        Returns:
            RecognitionResult or None: Updated recognition output if enough
            context has been processed, otherwise None.
        """
        array = np.asarray(frame)
        if array.size == 0:
            return None
        self._frames.append(array)

        total_samples = sum(chunk.size for chunk in self._frames)
        if total_samples < self._min_samples:
            return None

        signal = np.concatenate(self._frames)
        return self._service._recognize_signal(signal, self._config, self._threshold)

    def close(self) -> None:
        """
        Release buffered resources and finalize the recognition session.

        Implementations should flush pending frames and persist any state.
        """
        self._frames.clear()
