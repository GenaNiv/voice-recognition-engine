"""Simple live recognition runner using the shared service façade."""
from __future__ import annotations

import queue
import sys
from typing import Optional

import numpy as np
import sounddevice as sd

from file_management.bst import BinarySearchTree
from service.api import RecognitionConfig, VoiceRecognitionService


def run_live_recognition(
    base_directory: str = "test_environment",
    sample_rate: int = 16000,
    chunk_duration: float = 0.25,
    threshold: Optional[float] = None,
):
    """Capture microphone audio and stream it to the recognition service."""

    bst = BinarySearchTree()
    service = VoiceRecognitionService(bst=bst, base_directory=base_directory)
    config = RecognitionConfig(sample_rate=sample_rate)
    session = service.start_session(config=config, threshold=threshold)

    chunk_samples = max(1, int(chunk_duration * sample_rate))
    audio_queue: "queue.Queue[np.ndarray]" = queue.Queue()

    def _callback(indata, frames, time, status):  # pylint: disable=unused-argument
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(indata.copy().reshape(-1))

    print("Listening... Press Ctrl+C to stop.")
    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            blocksize=chunk_samples,
            dtype="float32",
            callback=_callback,
        ):
            latest = None
            while True:
                chunk = audio_queue.get()
                result = session.consume(chunk)
                if not result:
                    continue
                latest = result
                if result.speaker_id and not result.rejected:
                    print(f"Recognized {result.speaker_id} (score {result.score:.2f})")

    except KeyboardInterrupt:
        print("Stopping live recognition...")
    finally:
        session.close()
        bst.serialize_bst()


if __name__ == "__main__":
    run_live_recognition()
