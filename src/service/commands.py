# Updated commands.py based on the provided details

# commands.py
from service.api import (
    EnrollmentConfig,
    EnrollmentRequest,
    RecognitionConfig,
    RecognitionRequest,
    VoiceRecognitionService,
)
from service.audio_sources import WavFileSource

# Base Command class
class Command:
    """Base class for all commands."""
    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

# Command for enrolling a speaker
class EnrollSpeakerCommand(Command):
    def __init__(self, service: VoiceRecognitionService, speaker_name: str, audio_file: str, config: EnrollmentConfig):
        self.service = service
        self.speaker_name = speaker_name
        self.audio_file = audio_file
        self.config = config

    def execute(self):
        """Execute the enroll command by enrolling a new speaker."""
        frame_length = max(1, int(self.config.frame_size * self.config.sample_rate))
        source = WavFileSource(
            self.audio_file,
            frame_length=frame_length,
            sample_rate=self.config.sample_rate,
        )
        request = EnrollmentRequest(
            speaker_id=self.speaker_name,
            audio_source=source,
            config=self.config,
        )
        result = self.service.enroll(request)
        print(f"Speaker {result.speaker_id} enrolled successfully.")
        print(f"Model stored at: {result.model_path}")
        print(f"Metadata stored at: {result.metadata_path}")

# Command for recognizing a speaker
class RecognizeSpeakerCommand(Command):
    def __init__(self, service: VoiceRecognitionService, audio_file: str, config: RecognitionConfig, score_threshold: float | None):
        self.service = service
        self.audio_file = audio_file
        self.config = config
        self.score_threshold = score_threshold

    def execute(self):
        """Execute the recognize command to identify the speaker."""
        frame_length = max(1, int(self.config.frame_size * self.config.sample_rate))
        source = WavFileSource(
            self.audio_file,
            frame_length=frame_length,
            sample_rate=self.config.sample_rate,
        )
        request = RecognitionRequest(
            audio_source=source,
            threshold=self.score_threshold,
            config=self.config,
        )
        result = self.service.recognize(request)
        if result.speaker_id and not result.rejected:
            print(f"Recognized Speaker: {result.speaker_id} (score {result.score:.4f})")
        else:
            print("No speaker matched the provided audio.")


class RecognizeStreamCommand(Command):
    def __init__(self, service: VoiceRecognitionService, audio_file: str, config: RecognitionConfig, score_threshold: float | None, chunk_duration: float):
        self.service = service
        self.audio_file = audio_file
        self.config = config
        self.score_threshold = score_threshold
        self.chunk_duration = chunk_duration

    def execute(self):
        """Execute streaming recognition to simulate real-time processing."""
        session = self.service.start_session(config=self.config, threshold=self.score_threshold)
        frame_length = max(1, int(self.chunk_duration * self.config.sample_rate))
        source = WavFileSource(
            self.audio_file,
            frame_length=frame_length,
            sample_rate=self.config.sample_rate,
        )
        latest = None
        for chunk in source.stream():
            result = session.consume(chunk)
            if result:
                latest = result
                if result.speaker_id and not result.rejected:
                    print(f"Interim match: {result.speaker_id} (score {result.score:.4f})")
        session.close()

        if latest and latest.speaker_id and not latest.rejected:
            print(f"Final recognized speaker: {latest.speaker_id} (score {latest.score:.4f})")
        else:
            print("No speaker matched the streaming audio.")

# Command for listing all enrolled speakers
class ListSpeakersCommand(Command):
    def __init__(self, service: VoiceRecognitionService):
        self.service = service

    def execute(self):
        """Execute the list speakers command to display all speakers."""
        speakers = self.service.list_speakers()
        if not speakers:
            print("No speakers enrolled.")
            return

        print("Enrolled Speakers:")
        for speaker in speakers:
            print(f"- {speaker.speaker_id}: {speaker.metadata_path}")

# Command for deleting a speaker
class DeleteSpeakerCommand(Command):
    def __init__(self, service: VoiceRecognitionService, speaker_name: str):
        self.service = service
        self.speaker_name = speaker_name

    def execute(self):
        """Execute the delete command to remove a speaker."""
        self.service.delete_speaker(self.speaker_name)
        print(f"Speaker {self.speaker_name} deleted successfully.")

# CommandHandler to execute the commands
class CommandHandler:
    """Handles the execution of commands."""
    
    def run(self, command):
        """Run the given command."""
        command.execute()
