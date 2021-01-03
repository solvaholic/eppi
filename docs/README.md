# eppi

Learn to use a Waveshare e-Paper display with Raspberry Pi

## `/lib` and `/pic` from waveshare/e-Paper

Waveshare provides example code for their e-Paper displays on GitHub, and documentation on their wiki:

https://github.com/waveshare/e-Paper

https://www.waveshare.com/wiki/Main_Page

The `/lib` and `/pic` directory contents in this repository were copied from the Raspberry Pi Python section of **waveshare/e-Paper**.

Thank you, @waveshare, for providing this library and examples :bow:

## `/fonts` includes Tamzen font

PIL.ImageDraw appears to be happy with many different font formats. I figure monospace bitmap fonts will work most reliably on this display.

@Tecate provides [a catalog of bitmap fonts](https://github.com/Tecate/bitmap-fonts). I tried several and chose to work with Tamzen first:

https://github.com/sunaku/tamzen-font

In particular I like that Tamzen includes a variety of sizes in bold and regular. I find it also quite easy to read on the e-Paper display.

:hat-tip: @sunaku and Scott Fial, thank you for Tamzen and Tamsyn :bow:

# Screen size

A simple thing to do with a display is put text on it. To do that you may want to know how many rows and columns will fit.

Using Tamzen regular on a Waveshare [2.13inch e-Paper HAT](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT) V2 I found these dimensions:

| Font | Columns | Rows | Step |
|:- |:-:|:-:|:-:|
| Tamzen5x9r.bdf | 50 | 13 | 13 |
| Tamzen6x12r.bdf | 42 | 10 | 12 |
| Tamzen6x12r.bdf | 42 | 9 | 14 |
| Tamzen8x16r.bdf | 31 | 7 | 18 |
| Tamzen10x20r.bdf | 25 | 6 | 21 |

To demonstrate each of those I used Python like this, learning from Waveshare's examples on the way:

```python
# Tell PIL where to find the font
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'tamzen-font', 'bdf')
font16 = ImageFont.truetype(os.path.join(fontdir, 'Tamzen8x16r.bdf'), 16)

# Initialize the display
epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
epd.init(epd.PART_UPDATE)

# Create a new bitmap
image = Image.new('1', (250, 122), 255)  # 255: clear the frame    
draw = ImageDraw.Draw(image)

# Draw text onto the bitmap
mystring = '.........#'*6
myx = 1
for myy in range(1,122,18):
    draw.text((myx, myy), mystring, font = font16, fill = 0)

# Push the bitmap to the display
epd.displayPartial(epd.getbuffer(image))
```
