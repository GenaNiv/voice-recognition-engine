import argparse
import os

from file_management.bst import BinarySearchTree
from service.api import EnrollmentConfig, RecognitionConfig, VoiceRecognitionService
from service.commands import (
    EnrollSpeakerCommand,
    RecognizeSpeakerCommand,
    RecognizeStreamCommand,
    ListSpeakersCommand,
    DeleteSpeakerCommand,
    CommandHandler
)

def setup_environment(base_directory):
    # Ensure the base directory for models, audio files, and metadata exists
    if not os.path.exists(os.path.join(base_directory, "models")):
        os.makedirs(os.path.join(base_directory, "models"))
    if not os.path.exists(os.path.join(base_directory, "audio_files")):
        os.makedirs(os.path.join(base_directory, "audio_files"))
    if not os.path.exists(os.path.join(base_directory, "metadata")):
        os.makedirs(os.path.join(base_directory, "metadata"))
    print(f"Environment set up at {base_directory}")

def main(command_line_args=None):
    """CLI entry point."""
    # Initialize Argument Parser
    parser = argparse.ArgumentParser(description="Speaker Recognition CLI Tool")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    # Enroll Command with optional parameters for customization
    enroll_parser = subparsers.add_parser('enroll', help='Enroll a new speaker')
    enroll_parser.add_argument('speaker_name', type=str, help='Name of the speaker')
    enroll_parser.add_argument('audio_file', type=str, help='Path to the speaker audio file')

    # Optional arguments for speaker enrollment
    enroll_parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate of the audio file')
    enroll_parser.add_argument('--num_filters', type=int, default=26, help='Number of Mel filters')
    enroll_parser.add_argument('--num_ceps', type=int, default=13, help='Number of MFCC coefficients')
    enroll_parser.add_argument('--n_fft', type=int, default=512, help='FFT size for audio processing')
    enroll_parser.add_argument('--frame_size', type=float, default=0.025, help='Frame size in seconds')
    enroll_parser.add_argument('--frame_step', type=float, default=0.01, help='Frame step (overlap) in seconds')
    enroll_parser.add_argument('--n_mixtures', type=int, default=8, help='Number of Gaussian mixtures in GMM')

    # Recognize Command
    recognize_parser = subparsers.add_parser('recognize', help='Recognize a speaker from an audio file')
    recognize_parser.add_argument('audio_file', type=str, help='Path to the audio file')
    recognize_parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate of the audio file')
    recognize_parser.add_argument('--frame_size', type=float, default=0.025, help='Frame size in seconds')
    recognize_parser.add_argument('--frame_step', type=float, default=0.01, help='Frame step (overlap) in seconds')
    recognize_parser.add_argument('--fft_size', type=int, default=512, help='FFT size for audio processing')
    recognize_parser.add_argument('--num_filters', type=int, default=26, help='Number of Mel filters')
    recognize_parser.add_argument('--num_ceps', type=int, default=13, help='Number of MFCC coefficients')
    recognize_parser.add_argument('--score_threshold', type=float, default=None, help='Minimum log-likelihood to accept a speaker match')

    # Streaming recognition command
    recognize_stream_parser = subparsers.add_parser('recognize_stream', help='Stream audio chunks to recognize a speaker in near real-time')
    recognize_stream_parser.add_argument('audio_file', type=str, help='Path to the audio file')
    recognize_stream_parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate of the audio stream')
    recognize_stream_parser.add_argument('--frame_size', type=float, default=0.025, help='Frame size in seconds')
    recognize_stream_parser.add_argument('--frame_step', type=float, default=0.01, help='Frame step (overlap) in seconds')
    recognize_stream_parser.add_argument('--fft_size', type=int, default=512, help='FFT size for audio processing')
    recognize_stream_parser.add_argument('--num_filters', type=int, default=26, help='Number of Mel filters')
    recognize_stream_parser.add_argument('--num_ceps', type=int, default=13, help='Number of MFCC coefficients')
    recognize_stream_parser.add_argument('--score_threshold', type=float, default=None, help='Minimum log-likelihood to accept a speaker match')
    recognize_stream_parser.add_argument('--chunk_duration', type=float, default=0.5, help='Duration (seconds) of each streamed chunk')

    # List Speakers Command
    subparsers.add_parser('list_speakers', help='List all enrolled speakers')

    # Delete Speaker Command
    delete_parser = subparsers.add_parser('delete_speaker', help='Delete a speaker by name')
    delete_parser.add_argument('speaker_name', type=str, help='Name of the speaker to delete')

    # Parse the arguments
    args = parser.parse_args(command_line_args)

    # Initialize the command handler
    handler = CommandHandler()

    # Base directory setup
    base_directory = "test_environment"  # Placeholder for the base directory

    # Ensure environment setup
    setup_environment(base_directory)

    # Initialize Binary Search Tree and shared service
    bst = BinarySearchTree()
    service = VoiceRecognitionService(bst=bst, base_directory=base_directory)

    # Process the command based on the parsed arguments
    if args.command == 'enroll':
        enroll_config = EnrollmentConfig(
            sample_rate=args.sample_rate,
            num_filters=args.num_filters,
            num_ceps=args.num_ceps,
            fft_size=args.n_fft,
            frame_size=args.frame_size,
            frame_step=args.frame_step,
            mixtures=args.n_mixtures,
        )
        command = EnrollSpeakerCommand(
            service=service,
            speaker_name=args.speaker_name,
            audio_file=args.audio_file,
            config=enroll_config,
        )
        handler.run(command)

    elif args.command == 'recognize':
        recognize_config = RecognitionConfig(
            sample_rate=args.sample_rate,
            frame_size=args.frame_size,
            frame_step=args.frame_step,
            fft_size=args.fft_size,
            num_filters=args.num_filters,
            num_ceps=args.num_ceps,
        )
        command = RecognizeSpeakerCommand(
            service=service,
            audio_file=args.audio_file,
            config=recognize_config,
            score_threshold=args.score_threshold
        )
        handler.run(command)

    elif args.command == 'recognize_stream':
        recognize_config = RecognitionConfig(
            sample_rate=args.sample_rate,
            frame_size=args.frame_size,
            frame_step=args.frame_step,
            fft_size=args.fft_size,
            num_filters=args.num_filters,
            num_ceps=args.num_ceps,
        )
        command = RecognizeStreamCommand(
            service=service,
            audio_file=args.audio_file,
            config=recognize_config,
            score_threshold=args.score_threshold,
            chunk_duration=args.chunk_duration,
        )
        handler.run(command)

    elif args.command == 'list_speakers':
        command = ListSpeakersCommand(service=service)
        handler.run(command)

    elif args.command == 'delete_speaker':
        command = DeleteSpeakerCommand(service=service, speaker_name=args.speaker_name)
        handler.run(command)

    else:
        parser.print_help()

    # Persist BST state after command execution
    bst.serialize_bst()

if __name__ == "__main__":
    # To run with ad-hoc arguments during development, pass them explicitly, e.g.:
    # debug_args = [
    #     'recognize',
    #     '/path/to/audio.wav',
    #     '--sample_rate', '16000',
    # ]
    # main(debug_args)
    main()
