from fastapi import FastAPI, HTTPException, BackgroundTasks
import os
import uuid
from pydantic import BaseModel
from moviepy.editor import VideoFileClip, AudioFileClip
import subprocess

app = FastAPI()

# Directory to store generated videos and audio
OUTPUT_DIR = "generated_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class TextRequest(BaseModel):
    text: str

@app.post("/generate-video/")
async def generate_video(request: TextRequest, background_tasks: BackgroundTasks):
    """Generate AI video with lip-synced avatar from text."""
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Generate unique file names
    audio_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.wav")
    video_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.mp4")
    
    # Convert text to speech using Coqui-AI TTS
    tts_command = f"tts --text '{text}' --out_path {audio_path}"
    subprocess.run(tts_command, shell=True, check=True)
    
    # Generate AI avatar video with SadTalker
    sad_talker_command = f"python sadtalker/inference.py --driven_audio {audio_path} --result_dir {OUTPUT_DIR}"
    subprocess.run(sad_talker_command, shell=True, check=True)
    
    # Find generated video (assuming SadTalker outputs a video file in the output directory)
    generated_videos = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")]
    if not generated_videos:
        raise HTTPException(status_code=500, detail="Failed to generate video")
    
    final_video_path = os.path.join(OUTPUT_DIR, generated_videos[0])
    return {"video_url": f"/videos/{generated_videos[0]}"}

@app.get("/videos/{video_filename}")
def get_video(video_filename: str):
    """Serve generated video files."""
    video_path = os.path.join(OUTPUT_DIR, video_filename)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path, media_type="video/mp4")
