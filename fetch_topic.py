import json
import random
import os

def load_topics():
    with open('topics.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_used_topics():
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tips_and_tricks": [], "nutrition_facts": []}

def save_used_topics(used):
    with open('used_topics.json', 'w', encoding='utf-8') as f:
        json.dump(used, f, ensure_ascii=False, indent=2)

def get_next_topic():
    topics = load_topics()
    used = load_used_topics()
    
    # Alternate category each day based on total used count
    total_used = len(used["tips_and_tricks"]) + len(used["nutrition_facts"])
    category = "tips_and_tricks" if total_used % 2 == 0 else "nutrition_facts"
    
    available = [t for t in topics[category] if t["title"] not in used[category]]
    
    # If all used, reset that category's used list (cycle restart)
    if not available:
        used[category] = []
        available = topics[category]
    
    selected = random.choice(available)
    used[category].append(selected["title"])
    save_used_topics(used)
    
    return category, selected

if __name__ == "__main__":
    category, topic = get_next_topic()
    print(f"Category: {category}")
    print(f"Title: {topic['title']}")
    print(f"Script: {topic['hindi_script']}")
