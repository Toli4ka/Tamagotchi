from PIL import Image

def png_to_black_pixel_array(path):
    image = Image.open(path).convert("1")  # Convert to 1-bit (black and white)
    pixels = image.load()

    black_pixels = []
    width, height = image.size

    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0:  # type: ignore # 0 = black
                black_pixels.append((x, y))

    return black_pixels

# Example usage
path = "img/cat_5.png"
black_pixels = png_to_black_pixel_array(path)

# Print or export
print(black_pixels)