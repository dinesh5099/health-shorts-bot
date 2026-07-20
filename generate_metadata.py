import random

CORE_HASHTAGS = ["#FitSehatZone", "#Shorts", "#HealthTips", "#Fitness"]

TIPS_HASHTAGS = ["#DailyHealthTips", "#HealthyLifestyle", "#WellnessTips", 
                 "#MorningRoutine", "#SelfCare", "#HealthyHabits", "#MindAndBody"]

NUTRITION_HASHTAGS = ["#NutritionFacts", "#HealthyEating", "#IndianFood", 
                       "#HealthyDiet", "#FoodFacts", "#DesiFood", "#EatHealthy"]

GENERAL_HASHTAGS = ["#HealthyIndia", "#IndianLifestyle", "#Ayurveda", "#DesiHealth", "#FitIndia"]

def generate_title(topic_title):
    return f"{topic_title} | Health Tips in Hindi 🇮🇳 #Shorts"

def generate_hashtags(category, count=8):
    category_tags = TIPS_HASHTAGS if category == "tips_and_tricks" else NUTRITION_HASHTAGS
    selected = CORE_HASHTAGS + random.sample(category_tags, min(3, len(category_tags))) + random.sample(GENERAL_HASHTAGS, 2)
    return " ".join(selected[:count])

def generate_description(topic_title, engagement_text, category):
    hashtags = generate_hashtags(category)
    
    description = f"""{topic_title} 🌿

Daily health & nutrition tips for Indian lifestyle, explained simply.

✅ Science-backed advice
✅ Easy to follow daily habits
✅ Made for Indian audience

{engagement_text}

📌 Subscribe to FitSehatZone for daily health tips!
👉 Turn on notifications so you never miss a video

{hashtags}"""
    return description

if __name__ == "__main__":
    title = generate_title("Is Curd Good Every Day")
    desc = generate_description("Is Curd Good Every Day", "Do you eat curd every day? 🥣", "nutrition_facts")
    print(f"TITLE:\n{title}\n")
    print(f"DESCRIPTION:\n{desc}")
