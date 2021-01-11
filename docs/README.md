# eppi

Learn to use a Waveshare e-Paper display with Raspberry Pi

## Getting started

Many web sites provide answers and documentation about using Raspberry Pi. <https://raspberrypi.org> and <https://adafruit.com> are two I visit often.

If you can get Waveshare's [samples](https://github.com/waveshare/e-Paper) running then any introductory computer programming course using Python should equip you to to begin modifying them.

Here are the steps I took, to get a Waveshare [2.13inch e-Paper HAT](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT) V2 working with a Raspberry Pi 4B:

1. Install [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit) on the Pi.
1. Run `sudo raspi-config` to set locale, configure networking, enable SSH, and enable SPI
1. Install updates and additional packages:

    ```
    sudo apt update && sudo apt upgrade -y
    sudo apt install git python3-pip python3-pil python3-numpy
    sudo pip3 install RPi.GPIO
    sudo pip3 install spidev
    ```

1. Install BCM2835 libraries:

    ```
    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
    tar zxvf bcm2835-1.60.tar.gz 
    cd bcm2835-1.60/
    sudo ./configure
    sudo make
    sudo make check
    sudo make install
    #For more details, please refer to http://www.airspayce.com/mikem/bcm2835/
    ```

    These instructions :point_up: are from [Waveshare's wiki](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT).

1. Shut the Pi down, disconnect its power, and install the display. The HAT will sit right onto the Pi's GPIO header pins.

    In case you prefer to use the included dongle, connect the wires to the pins of the Pi as below:

    | Color | Name | Pin |
    |:-:|:-:|:-:|
    | Gray | VCC | 17 |
    | Brown | GND | 25 |
    | Blue | DIN | 19 |
    | Yellow | CLK | 23 |
    | Orange | CS | 24 |
    | Green | DC | 22 |
    | White | RST | 11 |
    | Purple | BUSY | 18 |

    See [Waveshare's wiki](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT) for complete details, and raspberrypi.org for [details about the GPIO header](https://www.raspberrypi.org/documentation/usage/gpio/README.md).

    After you get it hooked up, plug in the power and boot your Pi.

1. Clone the **waveshare/e-Paper** repository and run the example script:

    ```
    mkdir -p ~/repos && cd ~/repos
    git clone https://github.com/waveshare/e-Paper
    python3 e-Paper/RaspberryPi_JetsonNano/python/examples/epd_2in13_V2_test.py
    ```

At that point it should Just Work: The example script makes a series of images appear on the display.

## `/lib` and `/pic` from waveshare/e-Paper

Waveshare provides example code for their e-Paper displays on GitHub, and documentation on their wiki:

https://github.com/waveshare/e-Paper

https://www.waveshare.com/wiki/Main_Page

The `/lib` and `/pic` directory contents in this repository were copied from the Raspberry Pi Python section of **waveshare/e-Paper**.

Thank you, @waveshare, for providing this library and examples :bow:

## `/fonts` includes Tamzen font

This project uses PIL.ImageDraw to put text on the e-paper display. PIL.ImageDraw appears to be happy with many different font formats. This project uses the monospace bitmap font Tamzen:

https://github.com/sunaku/tamzen-font

In case you'd like to use other fonts, @Tecate provides [a catalog of bitmap fonts](https://github.com/Tecate/bitmap-fonts).

:hat-tip: @sunaku and Scott Fial, thank you for Tamzen and Tamsyn :bow:

## Screen size

A simple thing to do with a display is put text on it. To do that you may want to know how many rows and columns will fit.

Using Tamzen regular on a Waveshare [2.13inch e-Paper HAT](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT) V2 I found these dimensions:

| Font | Columns | Rows | Step | Box |
|:- |:-:|:-:|:-:|:-:|
| Tamzen5x9r.bdf | 50 | 13 | 13 | |
| Tamzen6x12r.bdf | 41 | 10 | 12 | 1,2 to 248,120 |
| Tamzen6x12r.bdf | 41 | 9 | 13 | 1,2 to 248,118 |
| Tamzen8x16r.bdf | 31 | 7 | 17 | 1,1 to 248,120 |
| Tamzen10x20r.bdf | 25 | 6 | 20 | 0,1 to 249,120 |

You can use Python like below to demonstrate different combinations of settings:

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

## `/eprint.py` and `/listen.sh`

`eprint.py` accepts a message on standard input (stdin) and displays it. For example:

```
echo 'Hello World!' | ./eprint.py
```

`listen.sh` does these three steps in order, in a loop, until it's interrupted:

1. Listen for input on UDP port 34567
1. When a message is received, run `eprint.py` to write it to the display
1. Wait 10 seconds

Use netcat to send a message to the listening server. On macOS or Linux terminal:

```
echo "YourMessageHere" | nc -u HOST 34567 -w0
```

Your implementation of netcat may balk at the `-w0`. You can try `-w1`, or just remove the option.

In Windows you can use `ncat` in place of `nc`. It's distributed with [nmap](https://nmap.org/download.html).
