from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_visual(title_text, category, output_path="visual.png"):
    # Vertical format for Shorts: 1080x1920
    width, height = 1080, 1920
    
    # Different color themes per category
    if category == "tips_and_tricks":
        bg_color = (20, 60, 90)      # Deep blue
        accent_color = (100, 200, 255)
    else:
        bg_color = (30, 90, 50)      # Deep green
        accent_color = (150, 255, 150)
    
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a bold font, fallback to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Category label at top
    category_label = "HEALTH TIP" if category == "tips_and_tricks" else "NUTRITION FACT"
    draw.text((width//2, 200), category_label, font=font_small, fill=accent_color, anchor="mm")
    
    # Wrap title text for readability
    wrapped_title = textwrap.fill(title_text, width=20)
    draw.text((width//2, height//2), wrapped_title, font=font_large, fill="white", anchor="mm", align="center")
    
    # Bottom branding placeholder
    draw.text((width//2, height-150), "Daily Health Tips", font=font_small, fill=accent_color, anchor="mm")
    
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    create_visual("Drink Water First Thing in Morning", "tips_and_tricks")
