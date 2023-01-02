import json
# Telegram chat export file
raw_data = open('./result.json', encoding="utf8")

clean_data = json.load(raw_data)

f = open("clean_messages.txt", "a", encoding="utf8")

allowed_msg_type = ['plain', 'link', 'hashtag', 'bold',
                    'italic', 'code', 'email', 'message', 'underline']

for message_entity in clean_data['messages']:
    for msg in message_entity['text_entities']:
        if not msg['type'] in allowed_msg_type or not msg["text"].strip():
            continue
        f.write(msg['text']+' ')
        print(msg)
f.close()
