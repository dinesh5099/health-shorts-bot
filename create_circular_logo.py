from PIL import Image, ImageDraw

def create_circular_logo_with_ring(input_path="logo.png", output_path="logo_circular.png", size=200, ring_color=(100, 200, 255), ring_width=6):
    img = Image.open(input_path).convert("RGBA")
    inner_size = size - (ring_width * 2)
    img = img.resize((inner_size, inner_size), Image.LANCZOS)
    
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(output)
    draw.ellipse((0, 0, size, size), fill=ring_color + (255,))
    
    mask = Image.new("L", (inner_size, inner_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, inner_size, inner_size), fill=255)
    
    output.paste(img, (ring_width, ring_width), mask=mask)
    output.save(output_path)
    return output_path

if __name__ == "__main__":
    create_circular_logo_with_ring()
