import json

QUESTION_STARTERS = ["Is ", "Does ", "Why ", "How ", "Should ", "Are ", "Can ", "What "]
QUESTION_EXCEPTIONS_KEEP_AS_IS = ["Why Cracking Knuckles Is Not Harmful", "Why Skipping Breakfast Is Harmful", 
                                    "Why Stretching After Waking Up Helps", "Why Walking After Meals Helps Digestion",
                                    "Why Sunlight Exposure Is Important", "Why You Should Limit Sugar Intake",
                                    "Why You Should Take Work Breaks", "How to Improve Your Posture",
                                    "How Stress Affects Your Body", "How Social Media Affects Mental Health",
                                    "Why Cold Showers May Be Beneficial", "Benefits of Journaling for Mental Health",
                                    "Why Regular Health Checkups Matter", "Why You Should Eat Seasonal Fruits",
                                    "Why Sleep Quality Affects Your Skin", "Why Stress Affects Your Skin and Hair",
                                    "How Stress Affects Your Skin and Hair", "Why You Should Never Skip Sunscreen",
                                    "How to Reduce Hair Fall Naturally", "Why Drinking Water Improves Your Skin",
                                    "Why Overwashing Your Face Can Be Harmful", "How to Improve Your Posture"]

def add_question_marks():
    with open('topics.json', 'r', encoding='utf-8') as f:
        topics = json.load(f)
    
    changed = 0
    for category in topics:
        for item in topics[category]:
            title = item['title']
            if title in QUESTION_EXCEPTIONS_KEEP_AS_IS:
                continue
            starts_with_question = any(title.startswith(qs) for qs in QUESTION_STARTERS)
            if starts_with_question and not title.endswith('?'):
                item['title'] = title + '?'
                changed += 1
    
    with open('topics.json', 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {changed} titles with question marks.")

if __name__ == "__main__":
    add_question_marks()
