import os
from src.service.speaker_enrollment import SpeakerEnrollment
from src.service.speaker_recognition import SpeakerRecognition
from src.file_management.bst import BinarySearchTree
from src.file_management.file_management import FileManagementInterface

def setup_environment(base_directory):
    # Ensure the base directory for models and metadata exists
    if not os.path.exists(os.path.join(base_directory, "models")):
        os.makedirs(os.path.join(base_directory, "models"))
    if not os.path.exists(os.path.join(base_directory, "audio_files")):
        os.makedirs(os.path.join(base_directory, "audio_files"))
    if not os.path.exists(os.path.join(base_directory, "metadata")):
        os.makedirs(os.path.join(base_directory, "metadata"))
    print(f"Test environment set up at {base_directory}")

def test_speaker_enrollment():
    base_directory = "./test_environment"
    bst = BinarySearchTree()

    # Initialize the SpeakerEnrollment system
    speaker_enrollment = SpeakerEnrollment(
        bst=bst,
        base_directory=base_directory
    )

    # Step 1: Set up environment
    setup_environment(base_directory)

    # Step 2: Test speaker enrollment
    #test_wav_file = os.path.join(base_directory, "audio_files", "sample_speaker.wav")
    test_wav_file ="/home/gena/PROJECTS/voice-recognition-engine/audio_files/gena.wav"

    # Simulate the existence of a wav file for testing
    #if not os.path.exists(test_wav_file):
    #    with open(test_wav_file, "w") as f:
    #        f.write("Simulated audio content")

    #Speaker 1
    speaker_name = "gena_speaker"
    enrollment_success = speaker_enrollment.enroll_speaker(speaker_name, test_wav_file)

    if enrollment_success:
        print("Speaker enrollment test passed.")
    else:
        print("Speaker enrollment test failed.")

    #Speaker 2
    test_wav_file ="/home/gena/PROJECTS/voice-recognition-engine/audio_files/women.wav"
    speaker_name = "women_speaker"
    enrollment_success = speaker_enrollment.enroll_speaker(speaker_name, test_wav_file)

    if enrollment_success:
        print("Speaker enrollment test passed.")
    else:
        print("Speaker enrollment test failed.")
    
    #Speaker 3
    test_wav_file ="/home/gena/PROJECTS/voice-recognition-engine/audio_files/man.wav"
    speaker_name = "men_speaker"
    enrollment_success = speaker_enrollment.enroll_speaker(speaker_name, test_wav_file)

    if enrollment_success:
        print("Speaker enrollment test passed.")
    else:
        print("Speaker enrollment test failed.")
        
    #Speaker 4
    test_wav_file ="/home/gena/PROJECTS/voice-recognition-engine/audio_files/leah.wav"
    speaker_name = "leah_speaker"
    enrollment_success = speaker_enrollment.enroll_speaker(speaker_name, test_wav_file)

    if enrollment_success:
        print("Speaker enrollment test passed.")
    else:
        print("Speaker enrollment test failed.")
        
    #Speaker 5
    test_wav_file ="/home/gena/PROJECTS/voice-recognition-engine/audio_files/maria.wav"
    speaker_name = "maria_speaker"
    enrollment_success = speaker_enrollment.enroll_speaker(speaker_name, test_wav_file)

    if enrollment_success:
        print("Speaker enrollment test passed.")
    else:
        print("Speaker enrollment test failed.")
        
    # Step 3: Verify file management system
    file_manager = speaker_enrollment.file_manager

    # List all stored files
    all_files = file_manager.list_all_files()
    print("\nStored Files Metadata:")
    for file_metadata in all_files:
        print(file_metadata)
    
    # Step 4: Test speaker recognition
    test_wav_file ="/home/gena/PROJECTS/voice-recognition-engine/audio_files/maria_recognize.wav"
    speaker_name = "maria_speaker"
    speaker_recognition = SpeakerRecognition(
        bst=bst,
        base_directory=base_directory,
        sample_rate=16000,
        frame_size=0.025,
        frame_step=0.01,
        fft_size=512,
        num_filters=26,
        num_ceps=13,
    )

    recognized_speaker = speaker_recognition.recognize_speaker(test_wav_file)
    
    if recognized_speaker == speaker_name:
        print("Speaker recognition test passed.")
    else:
        print(f"Speaker recognition test failed. Expected: {speaker_name}, but got: {recognized_speaker}")

if __name__ == "__main__":
    test_speaker_enrollment()
