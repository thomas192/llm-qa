from youtube_transcript_api import YouTubeTranscriptApi
import os

from format_transcripts import format_transcripts

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_video_id(url):
    return url.rsplit("=", 1)[-1].split("&", 1)[0]

def save_transcript(video_id, transcript, db_name):
    dir_path = os.path.join(DATA_DIR, db_name)
    os.makedirs(dir_path, exist_ok=True)
    filename = f"{dir_path}/{video_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for entry in transcript:
            f.write(entry["text"] + "\n")
            
def get_transcripts(links, db_name):
    video_urls = [url for url in links.split("\n") if url]
    print(video_urls)

    for url in video_urls:
        video_id = get_video_id(url)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            save_transcript(video_id, transcript, db_name)
        except Exception as e:
            print(f"An error occurred with video {video_id}: {e}")
            
    format_transcripts(db_name)
