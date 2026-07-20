import json
import os
from send_alert import send_email

def count_remaining_topics():
    with open('topics.json', 'r', encoding='utf-8') as f:
        topics = json.load(f)
    
    if os.path.exists('used_topics.json'):
        with open('used_topics.json', 'r', encoding='utf-8') as f:
            used = json.load(f)
    else:
        used = {"tips_and_tricks": [], "nutrition_facts": []}
    
    total_topics = len(topics['tips_and_tricks']) + len(topics['nutrition_facts'])
    total_used = len(used['tips_and_tricks']) + len(used['nutrition_facts'])
    remaining = total_topics - total_used
    
    return remaining

def check_and_alert():
    remaining = count_remaining_topics()
    print(f"Remaining topics: {remaining}")
    
    if remaining <= 15:
        subject = f"⚠️ FitSehatZone: Only {remaining} topics left!"
        body = f"""Hi,

Your topics.json has only {remaining} unused topics remaining.
At 3 videos/day, this covers approximately {remaining // 3} more days.

Please add more topics soon to avoid content repeats.

- FitSehatZone Bot"""
        send_email(subject, body)

if __name__ == "__main__":
    check_and_alert()
