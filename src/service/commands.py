# Updated commands.py based on the provided details

# commands.py
import os
from service.speaker_enrollment import SpeakerEnrollment
from service.speaker_recognition import SpeakerRecognition
from file_management.file_management import FileManagementInterface

# Base Command class
class Command:
    """Base class for all commands."""
    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

# Command for enrolling a speaker
class EnrollSpeakerCommand(Command):
    def __init__(self, speaker_name, audio_file, bst, base_directory, 
                 sample_rate, num_filters, num_ceps, n_fft, 
                 frame_size, frame_step, n_mixtures):
        self.speaker_name = speaker_name
        self.audio_file = audio_file
        self.bst = bst
        self.base_directory = base_directory
        self.sample_rate = sample_rate
        self.num_filters = num_filters
        self.num_ceps = num_ceps
        self.n_fft = n_fft
        self.frame_size = frame_size
        self.frame_step = frame_step
        self.n_mixtures = n_mixtures

    def execute(self):
        """Execute the enroll command by enrolling a new speaker."""
        # Initialize SpeakerEnrollment with the provided parameters
        speaker_enrollment = SpeakerEnrollment(
            bst=self.bst, 
            base_directory=self.base_directory, 
            sample_rate=self.sample_rate, 
            num_filters=self.num_filters, 
            num_ceps=self.num_ceps, 
            n_fft=self.n_fft, 
            frame_size=self.frame_size, 
            frame_step=self.frame_step, 
            n_mixtures=self.n_mixtures
        )

        # Enroll the speaker using the provided parameters
        success = speaker_enrollment.enroll_speaker(self.speaker_name, self.audio_file)
        if success:
            print(f"Speaker {self.speaker_name} enrolled successfully.")
        else:
            print(f"Failed to enroll speaker {self.speaker_name}.")

# Command for recognizing a speaker
class RecognizeSpeakerCommand(Command):
    def __init__(self, bst, audio_file, base_directory, sample_rate, frame_size, frame_step, fft_size, num_filters, num_ceps):
        self.audio_file = audio_file
        self.recognizer = SpeakerRecognition(
            bst=bst,
            base_directory=base_directory,
            sample_rate=sample_rate,
            frame_size=frame_size,
            frame_step=frame_step,
            fft_size=fft_size,
            num_filters=num_filters,
            num_ceps=num_ceps
        )

    def execute(self):
        """Execute the recognize command to identify the speaker."""
        recognized_speaker = self.recognizer.recognize_speaker(self.audio_file)
        print(f"Recognized Speaker: {recognized_speaker}")

# Command for listing all enrolled speakers
class ListSpeakersCommand(Command):
    def __init__(self, file_management):
        self.file_management = file_management

    def execute(self):
        """Execute the list speakers command to display all speakers."""
        speakers = self.file_management.list_all_files()
        print("Enrolled Speakers:")
        for speaker in speakers:
            print(f"- {speaker['file_id']}")

# Command for deleting a speaker
class DeleteSpeakerCommand(Command):
    def __init__(self, speaker_name, file_management):
        self.speaker_name = speaker_name
        self.file_management = file_management

    def execute(self):
        """Execute the delete command to remove a speaker."""
        self.file_management.delete_file(self.speaker_name)
        print(f"Speaker {self.speaker_name} deleted successfully.")

# CommandHandler to execute the commands
class CommandHandler:
    """Handles the execution of commands."""
    
    def run(self, command):
        """Run the given command."""
        command.execute()