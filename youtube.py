from youtube_transcript_api import YouTubeTranscriptApi
import os

MAX_LINE_LENGTH = 30
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
    
    format_transcripts(db_name, video_id)
    
def format_transcripts(db_name, video_id):
    filename = f"{db_name}/{video_id}.txt"
    filepath = os.path.join(DATA_DIR, filename)
        
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
            
    formatted_lines = []
    current_line = ""
    for line in lines:
        line = line.strip()
        if len(line) < MAX_LINE_LENGTH:
            current_line += " " + line
            formatted_lines.append(current_line.strip())
            current_line = ""
        else:
            current_line += " " + line
    if current_line:
        formatted_lines.append(current_line.strip())
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(formatted_lines))

def get_transcripts_from_youtube(links, db_name):
    video_urls = [url for url in links.split("\n") if url]

    for url in video_urls:
        video_id = get_video_id(url)
        try:
            print(f"[*] Retrieving transcript {url}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            save_transcript(video_id, transcript, db_name)
        except Exception as e:
            print(f"An error occurred with video {video_id}: {e}")
