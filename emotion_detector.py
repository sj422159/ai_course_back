import threading
import subprocess

def run_face_emotion():
    """Run the facial emotion detection script."""
    subprocess.run(["python", "face_detection.py"])

def run_voice_emotion():
    """Run the voice emotion detection script."""
    subprocess.run(["python", "voice_emotion.py"])

if __name__ == "__main__":
    face_thread = threading.Thread(target=run_face_emotion)
    voice_thread = threading.Thread(target=run_voice_emotion)

    face_thread.start()
    voice_thread.start()

    face_thread.join()
    voice_thread.join()
