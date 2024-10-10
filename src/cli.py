import argparse
import os

from service.commands import (
    EnrollSpeakerCommand,
    RecognizeSpeakerCommand,
    ListSpeakersCommand,
    DeleteSpeakerCommand,
    CommandHandler
)
from file_management.bst import BinarySearchTree
from file_management.file_management import FileManagementInterface

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

    # Initialize Binary Search Tree
    bst = BinarySearchTree()  # Placeholder for actual binary search tree implementation

    # Process the command based on the parsed arguments
    if args.command == 'enroll':
        command = EnrollSpeakerCommand(
            speaker_name=args.speaker_name,
            audio_file=args.audio_file,
            bst=bst,
            base_directory=base_directory,
            sample_rate=args.sample_rate,
            num_filters=args.num_filters,
            num_ceps=args.num_ceps,
            n_fft=args.n_fft,
            frame_size=args.frame_size,
            frame_step=args.frame_step,
            n_mixtures=args.n_mixtures
        )
        handler.run(command)
        
        # Serialize the BST before exiting the program
        bst.serialize_bst()

    elif args.command == 'recognize':
        command = RecognizeSpeakerCommand(
            bst=bst,
            audio_file=args.audio_file,
            base_directory=base_directory,
            sample_rate=args.sample_rate,
            frame_size=args.frame_size,
            frame_step=args.frame_step,
            fft_size=args.fft_size,
            num_filters=args.num_filters,
            num_ceps=args.num_ceps
        )
        handler.run(command)

    elif args.command == 'list_speakers':
        file_management = FileManagementInterface(bst=bst, base_directory=base_directory)
        command = ListSpeakersCommand(file_management)
        handler.run(command)

    elif args.command == 'delete_speaker':
        file_management = FileManagementInterface(bst=bst, base_directory=base_directory)
        command = DeleteSpeakerCommand(args.speaker_name, file_management)
        handler.run(command)

    else:
        parser.print_help()

if __name__ == "__main__":
    #debug_args = [
    #    'enroll',
    #    'maria',
    #    '/home/gena/PROJECTS/voice-recognition-engine/audio_files/maria.wav',
    #    '--sample_rate', '16000',
    #    '--num_filters', '40',
    #    '--num_ceps', '13',
    #    '--n_fft', '512',
    #    '--frame_size', '0.025',
    #    '--frame_step', '0.01',
    #    '--n_mixtures', '8'
    #]
    
    debug_args = [
        'recognize',
        '/home/gena/PROJECTS/voice-recognition-engine/audio_files/leah_recognize.wav',
        '--sample_rate', '16000',
        '--frame_size', '0.025',
        '--frame_step', '0.01',
        '--fft_size', '512',
        '--num_filters', '40',
        '--num_ceps', '13',
    ]

    main(debug_args)