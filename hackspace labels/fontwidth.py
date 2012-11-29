from PIL import Image, ImageDraw, ImageFont
colour = 'white'
text = 'One-hand'
font = ImageFont.truetype("/usr/share/fonts/truetype/thai/TlwgTypo-Bold.ttf", 10)
im = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
w, h = draw.textsize(text)
print w, h
