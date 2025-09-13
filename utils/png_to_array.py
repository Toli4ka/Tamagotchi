from PIL import Image # type: ignore
from pathlib import Path

def png_to_black_pixel_array(path):
    """Convert a PNG file to an array of black pixel coordinates (tuple)."""
    image = Image.open(path).convert("1")  # Convert to 1-bit (black and white)
    pixels = image.load()

    black_pixels = []
    width, height = image.size

    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0:  # type: ignore # 0 = black
                black_pixels.append((x, y))

    return black_pixels

def png_to_black_pixel_bytearray(path):
    """Convert a PNG file to a byte array of black pixel coordinates."""
    black_pixels = png_to_black_pixel_array(path)
    byte_array = bytearray()
    for x, y in black_pixels:
        byte_array.append(x)
        byte_array.append(y)
    return byte_array

def png_to_bytearray(path):
    """Convert a 64x64 PNG file to a byte array compatible with framebuf.MONO_HLSB."""
    image = Image.open(path).convert("1")
    width, height = image.size
    # assert width == 64 and height == 64, "Image must be 64x64"
    assert width % 8 == 0 and height % 8 == 0, "Image width and height must be multiples of 8"
    msb_bytes = image.tobytes()
    inverted_bytes = bytearray(~b & 0xFF for b in msb_bytes)
    return inverted_bytes

# # Example usage
# path = "img/coffee/coffee0.png"
# black_pixels = png_to_black_pixel_array(path)
# byte_array = png_to_black_pixel_bytearray(path)
# byte_array_framebuf, width, height = png_to_bytes(path)
# # Print or export
# # print(black_pixels)
# # print(list(byte_array))
# print(list(byte_array_framebuf))
# # Each tuple has 2 integers, each integer is 2 bytes
# print(f"Array size: {len(black_pixels) * 2 * 2} Bytes")  
# print(f"Bytearray size: {len(byte_array)} Bytes")  # Each integer is 1 byte
# print(f"Framebuf bytearray size: {len(byte_array_framebuf)} Bytes")  # Each integer is 1 byte


def main(img_folder="img", output_file="png_bytearrays.txt"):
    img_folder = Path(img_folder)
    lines = []
    for png_path in img_folder.rglob("*.png"):
        name = png_path.stem
        ba = png_to_bytearray(png_path)
        line = f"{name}=bytearray({list(ba)})"
        lines.append(line)
    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"Done! Saved {len(lines)} bytearrays to {output_file}")

if __name__ == "__main__":
    # path = "img/coffee/coffee0.png"
    # ba = png_to_bytearray(path)
    # print(list(ba))
    main()