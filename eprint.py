#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
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
