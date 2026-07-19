import json

for line in open('C:/Users/praty/.gemini/antigravity/brain/99f5258f-08cc-436f-9f75-75732744ffd5/.system_generated/logs/transcript.jsonl', encoding='utf-8'):
    if 'Unhandled exception' in line:
        data = json.loads(line)
        if 'content' in data and 'Traceback' in data['content']:
            print(data['content'][:4000])
