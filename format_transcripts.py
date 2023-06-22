import os

DATA_DIR = "data"

MAX_LINE_LENGTH = 30

def format_transcripts(db_name):
    dir_path = os.path.join(DATA_DIR, db_name)
    
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        
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
