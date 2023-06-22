from youtube_transcript_api import YouTubeTranscriptApi
import os

DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def get_video_id(url):
    return url.rsplit('=', 1)[-1].split('&', 1)[0]

def save_transcript(video_id, transcript):
    filename = f"{DATA_DIR}/{video_id}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in transcript:
            f.write(entry['text'] + '\n')

with open("urls.txt", 'r') as f:
    video_urls = [line.strip() for line in f]

for url in video_urls:
    video_id = get_video_id(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        save_transcript(video_id, transcript)
    except Exception as e:
        print(f"An error occurred with video {video_id}: {e}")
