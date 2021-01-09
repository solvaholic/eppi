#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import textwrap
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    # Get mystring early, to block processing til stdio ends
    mystring = sys.stdin.read()

    # Tell PIL where to find fonts
    fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'tamzen-font', 'bdf')
    font12 = ImageFont.truetype(os.path.join(fontdir, 'Tamzen6x12r.bdf'), 12)
    font12b = ImageFont.truetype(os.path.join(fontdir, 'Tamzen6x12b.bdf'), 12)
    font16 = ImageFont.truetype(os.path.join(fontdir, 'Tamzen8x16r.bdf'), 16)
    font16b = ImageFont.truetype(os.path.join(fontdir, 'Tamzen8x16b.bdf'), 16)
    font20 = ImageFont.truetype(os.path.join(fontdir, 'Tamzen10x20r.bdf'), 20)
    font20b = ImageFont.truetype(os.path.join(fontdir, 'Tamzen10x20b.bdf'), 20)

    # Initialize the display
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.init(epd.PART_UPDATE)

    # Create a new bitmap
    image = Image.new('1', (250, 122), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)

    # Set the message to be displayed
    if mystring == "":
        # stdin was empty, so set mystring manually
        mystring = 'All work and no play makes Jack a dull boy. '*18

    # Set which font to use
    myfont = font20b

    # How wide and high is a character in this font?
    charW, charH = myfont.getsize('#')

    # Figure origin and dimensions based on size of character
    xyUL = ( int(250%charW/2), int(122%charH/2) )
    maxCols = int(250/charW)
    maxRows = int(122/charH)

    # Draw text onto the bitmap
    mylines = textwrap.TextWrapper(width=maxCols).wrap(mystring)
    curLine = 0
    for line in mylines:
        curXy = (xyUL[0], charH*curLine+xyUL[1])
        draw.text(curXy, line, font = myfont, fill = 0)
        curLine = curLine + 1
        if curLine >= maxRows:
            break
    
    # Push the bitmap to the display
    epd.displayPartial(epd.getbuffer(image))

    logging.info("Goto Sleep...")
    epd.sleep()
    time.sleep(3)
    epd.Dev_exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
