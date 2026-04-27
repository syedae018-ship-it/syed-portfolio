from PIL import Image

img = Image.open('character.png')
img = img.convert('RGBA')
w, h = img.size
print(f"Image size: {w}x{h}")

for x in range(w-1, -1, -1):
    found = False
    for y in range(h):
        r, g, b, a = img.getpixel((x, y))
        if a > 0 and b > 200 and r < 100 and g < 150:
            print(f"Right-most blue pixel at: {x}, {y}")
            found = True
            break
    if found:
        break
