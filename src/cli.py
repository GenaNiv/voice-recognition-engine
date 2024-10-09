import argparse
from service.commands import EnrollSpeakerCommand, RecognizeSpeakerCommand, ListSpeakersCommand, DeleteSpeakerCommand, CommandHandler
from bst import BinarySearchTree

def main():
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

    # List Speakers Command
    subparsers.add_parser('list_speakers', help='List all enrolled speakers')

    # Delete Speaker Command
    delete_parser = subparsers.add_parser('delete_speaker', help='Delete a speaker by name')
    delete_parser.add_argument('speaker_name', type=str, help='Name of the speaker to delete')

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the command handler
    handler = CommandHandler()

    # Binary Search Tree and base directory
    bst = BinarySearchTree()  # Placeholder for actual binary search tree
    base_directory = "models/"  # Placeholder for actual base directory

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

    elif args.command == 'recognize':
        command = RecognizeSpeakerCommand(args.audio_file)
        handler.run(command)

    elif args.command == 'list_speakers':
        command = ListSpeakersCommand()
        handler.run(command)

    elif args.command == 'delete_speaker':
        command = DeleteSpeakerCommand(args.speaker_name)
        handler.run(command)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
