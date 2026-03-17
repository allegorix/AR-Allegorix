from PIL import Image

def process_card(input_path, output_path, size=512):
    try:
        # Open the image
        img = Image.open(input_path).convert('RGB')
        
        # Instead of padding with white to make a square, AR.js markers work best 
        # when the image fills as much of the inner square as possible.
        # Let's crop/resize the business card to fill the 512x512 square so the tracking features are large.
        
        # Calculate aspect ratio preserving resize, but FILL the square (crop excess)
        w, h = img.size
        # We want to fill 512x512, so resize such that the MINIMUM dimension matches 512
        ratio = max(size / w, size / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Crop the center to exactly 512x512
        left = (new_w - size) // 2
        top = (new_h - size) // 2
        right = left + size
        bottom = top + size
        
        new_img = img.crop((left, top, right, bottom))
        
        # Note: the pymarker generator will add a black border around this inner image
        new_img.save(output_path)
        print(f"Successfully processed card to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

process_card("card.png", "card-inner.png")
