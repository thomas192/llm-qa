import os

DATA_DIR = 'data'

max_line_length = 30

for filename in os.listdir(DATA_DIR):
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    formatted_lines = []
    current_line = ''
    for line in lines:
        line = line.strip()
        if len(line) < max_line_length:
            current_line += ' ' + line
            formatted_lines.append(current_line.strip())
            current_line = ''
        else:
            current_line += ' ' + line
    if current_line:
        formatted_lines.append(current_line.strip())
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(formatted_lines))
