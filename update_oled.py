# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
from datetime import datetime
import subprocess

import board 
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_si7021


# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
sensor = adafruit_si7021.SI7021(i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)


# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Shell scripts for system monitoring from here:
# https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell=True).decode("utf-8")


cmd_wttr = 'curl wttr.in/30067?format="%C+%t&m"'
wttr = subprocess.check_output(cmd_wttr, shell=True).decode("utf-8")

SCREEN_UPDATE = 30 #in sec
MINUTE_LOG = 60/SCREEN_UPDATE
PERIOD_LOG = 30 #in mins

screen_counter = 1
min_counter = 1

sum_temp = 0.0
sum_min_temp = 0.0
sum_humi = 0.0
sum_min_humi = 0.0

temp = sensor.temperature
humi = sensor.relative_humidity
draw.text((x, top), wttr, fill=255)
draw.text((x+5, top+8), "Hmdt: %0.1f %%" % humi, fill=255)
draw.text((x+5, top+16), "Tmp: %0.1f C" % temp, fill=255)
draw.text((x+5, top+24), "   : %0.1f F" % ((temp*1.8)+32), fill=255)
disp.image(image)
disp.show()


while True:
    temp = sensor.temperature
    humi = sensor.relative_humidity

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top), wttr, fill=255)
    draw.text((x+5, top+8), "Hmdt: %0.1f %%" % humi, fill=255)
    draw.text((x+5, top+16), "Tmp: %0.1f C" % temp, fill=255)
    draw.text((x+5, top+24), "   : %0.1f F" % ((temp*1.8)+32), fill=255)
    disp.image(image)
    disp.show()
    time.sleep(SCREEN_UPDATE)

    sum_temp = sum_temp + temp
    sum_humi = sum_humi + humi
    #one minute has passed
    if screen_counter==MINUTE_LOG:
        screen_counter = 0
        sum_min_temp = sum_min_temp + sum_temp/MINUTE_LOG
        sum_min_humi = sum_min_humi + sum_humi/MINUTE_LOG
        sum_temp = 0.0
        sum_humi = 0.0
        
        #log mins data
        if min_counter==PERIOD_LOG:
            #sometimes cannot get the ip in startup
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell=True).decode("utf-8")

            cmd_wttr = 'curl wttr.in/30067?format="%C+%t&m"'
            wttr = subprocess.check_output(cmd_wttr, shell=True).decode("utf-8")

            min_counter = 0
            half_hr_temp = sum_min_temp/PERIOD_LOG
            half_hr_humi = sum_min_humi/PERIOD_LOG
            sum_min_temp = 0.0
            sum_min_humi = 0.0
            now = datetime.now()

            f=open("/home/pi/data_logs.csv","a",4)
            f.write("%s, %0.1f, %0.1f, %s\n" 
                    % (now.strftime("%d-%m-%Y %H:%M"), half_hr_temp, half_hr_humi, wttr))
            f.flush()
            f.close()
        
        min_counter=min_counter + 1
    screen_counter = screen_counter + 1

     
