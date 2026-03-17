from PIL import Image, ImageDraw

def process_card(input_path, inner_output, marker_output, inner_size=512):
    try:
        # Open the image
        img = Image.open(input_path).convert('RGB')
        
        # 1. Create inner pattern image
        # Instead of cropping, we will shrink the business card to fit inside the square.
        w, h = img.size
        # To fit inside 512x512 without cropping:
        ratio = min(inner_size / w, inner_size / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Create a white background
        inner_img = Image.new('RGB', (inner_size, inner_size), 'white')
        
        # Paste the resized card in the center
        left = (inner_size - new_w) // 2
        top = (inner_size - new_h) // 2
        inner_img.paste(img_resized, (left, top))
        
        # Save inner pattern image
        inner_img.save(inner_output)
        print(f"Successfully processed inner pattern to {inner_output}")
        
        # 2. Create the full scannable marker image with the black border
        # AR.js patternRatio defaults to 0.5 (inner image is 50% of the total width)
        # That means border width is 25% of the total width.
        # But wait! A standard marker is: target size e.g. 1024, black border from 0 to 1024?
        # Actually standard AR.js generator uses a black square, with the inner image inside it.
        # Default AR.js pattern ratio = 0.5. 
        # So if total is 1024: inner is 512, border padding is 256 on all sides.
        marker_size = int(inner_size / 0.5) # 1024
        marker_img = Image.new('RGB', (marker_size, marker_size), 'white')
        
        draw = ImageDraw.Draw(marker_img)
        # Draw the thick black square
        border_thickness = int(marker_size * 0.25)
        # The black square goes from border_thickness to marker_size - border_thickness
        # Actually, let's just draw a large black rectangle and paste the inner_img centered.
        # Wait, the black border is the outer part? No, typical AR marker has a thick black border, with white padding OUTSIDE the black border!
        # Standard: white 1024x1024. Black square covering the center. Inner image covering the center of that.
        # Actually, usually there's a small white outline or none. Let's just make the whole background white, draw a black square of size 512*1.5 = 768?
        # No, a standard marker is usually printed on white paper. The black square is the distinguishing feature.
        # If pattern ratio = 0.5, the black square's width is marker_size. Inner width is 0.5 * marker_size.
        
        # So black square is from 0 to marker_size, and inner image is in the center.
        # BUT let's add some white padding outside so it's easy to see where the border ends.
        canvas_size = marker_size + 200
        canvas_img = Image.new('RGB', (canvas_size, canvas_size), 'white')
        
        # Draw black square
        black_square = Image.new('RGB', (marker_size, marker_size), 'black')
        canvas_img.paste(black_square, (100, 100))
        
        # Paste inner image
        # Inner image size is inner_size (512). Marker size is 1024.
        # Center of canvas is canvas_size // 2
        canvas_img.paste(inner_img, (100 + (marker_size - inner_size) // 2, 100 + (marker_size - inner_size) // 2))
        
        canvas_img.save(marker_output)
        print(f"Successfully generated full marker to {marker_output}")
        
    except Exception as e:
        print(f"Error: {e}")

process_card("card.png", "card-inner.png", "card-marker.png")
