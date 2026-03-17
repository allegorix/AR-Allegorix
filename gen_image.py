import sys
from PIL import Image, ImageDraw, ImageFont

def create_marker_image(text, output_path, size=512):
    # Create white square
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw black border (default AR.js border size is 1/6 of the total width)
    # However, pattern generator uses a different convention. 
    # Usually we generate the INNER pattern as 16x16 or a square, and AR.js recognizes it.
    # Wait, the `pymarker` tool expects the INNER image, or the whole image?
    # Actually, let's just create the inner pattern: white background with "Allegorix" text.
    # Let's make a square image.
    
    # We will just write the text in the middle
    try:
        # Try to load a nice font
        font = ImageFont.truetype("/usr/share/fonts/noto/NotoSans-Bold.ttf", 180)
    except IOError:
        font = ImageFont.load_default()

    # Get text size
    # In newer Pillow versions, textsize is removed. Use textbbox.
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (size - text_w) / 2
    y = (size - text_h) / 2
    
    draw.text((x, y), text, font=font, fill='black')
    
    img.save(output_path)
    print(f"Saved {output_path}")

create_marker_image("Allegorix", "allegorix-inner.png")
