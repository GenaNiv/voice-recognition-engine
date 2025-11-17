"""Concrete AudioSource implementations."""
from __future__ import annotations

from typing import Iterable

import librosa
import numpy as np

from service.api import AudioSource


class WavFileSource(AudioSource):
    """Reads frames from a wav file for batch processing."""

    def __init__(self, path: str, frame_length: int = 1600, sample_rate: int = 16000):
        """
        Prepare a file-backed audio source.

        Args:
            path: Filesystem path to the wav file.
            frame_length: Number of samples per emitted frame.
            sample_rate: Target sample rate for loading via librosa.
        """
        self.path = path
        self.frame_length = frame_length
        self.sample_rate = sample_rate

    def stream(self) -> Iterable[np.ndarray]:
        """
        Iterate through the wav file and yield PCM frames.

        Returns:
            Iterable[np.ndarray]: successive chunks ready for processing.
        """
        signal, _ = librosa.load(self.path, sr=self.sample_rate)
        for start in range(0, len(signal), self.frame_length):
            yield np.asarray(signal[start:start + self.frame_length])


class BufferAudioSource(AudioSource):
    """Yields supplied buffers directly (useful for live integrations)."""

    def __init__(self, buffers: Iterable[np.ndarray]):
        """
        Initialize the source with an iterable of PCM buffers.

        Args:
            buffers: Iterable yielding audio frames captured elsewhere.
        """
        self._buffers = buffers

    def stream(self) -> Iterable[np.ndarray]:
        """
        Yield each provided buffer in order.

        Returns:
            Iterable[np.ndarray]: passthrough of supplied frames.
        """
        for chunk in self._buffers:
            yield np.asarray(chunk)
