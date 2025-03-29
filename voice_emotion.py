import os
import asyncio
import pyaudio
from deepgram import Deepgram
from dotenv import load_dotenv
from queue import Queue

# Load environment variables from .env file
load_dotenv()

# Get API key from .env
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("Deepgram API key is missing. Set it in a .env file.")

# Initialize Deepgram client
deepgram = Deepgram(DEEPGRAM_API_KEY)

# Audio settings
FORMAT = pyaudio.paInt16  # 16-bit audio
CHANNELS = 1  # Mono audio
RATE = 16000  # Sampling rate (16kHz recommended for Deepgram)
CHUNK = 1024  # Buffer size

# Queue for storing audio chunks
audio_queue = Queue()


async def analyze_real_time_audio():
    """Continuously captures and analyzes real-time audio sentiment."""
    try:
        print("🎙️ Listening for real-time sentiment analysis... (Press Ctrl+C to stop)")

        # Open microphone stream
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        while True:
            audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
            audio_queue.put(audio_chunk)

            # Convert audio data to Deepgram format
            source = {"buffer": audio_chunk, "mimetype": "audio/wav"}
            response = await deepgram.transcription.prerecorded(source, {"smart_format": True})

            # **FIX: Handle NoneType error**
            if not response or "results" not in response or not response["results"]["channels"]:
                print("⚠️ Warning: No valid response from Deepgram")
                continue  # Skip to next iteration
            
            # Extract transcript safely
            transcript = response["results"]["channels"][0]["alternatives"][0].get("transcript", "")

            # **Check if transcript is empty**
            if not transcript:
                print("⚠️ No speech detected or unclear audio.")
                continue  # Skip to next iteration

            # Emotion classification logic
            if "frustrated" in transcript or "difficult" in transcript:
                detected_emotion = "trying hard to solve"
            elif "sad" in transcript or "upset" in transcript:
                detected_emotion = "sad"
            elif "confused" in transcript or "not sure" in transcript:
                detected_emotion = "confused"
            else:
                detected_emotion = "happy"

            print(f"🟢 Detected Emotion: {detected_emotion}")

    except Exception as e:
        print(f"❌ Error in real-time audio analysis: {e}")

    finally:
        print("🔴 Stopping audio stream...")
        stream.stop_stream()
        stream.close()
        p.terminate()


# Run the real-time audio sentiment detection
if __name__ == "__main__":
    asyncio.run(analyze_real_time_audio())
