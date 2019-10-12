import time
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

cmd = "cat /sys/class/net/wlan0/address"
MAC = subprocess.check_output(cmd, shell=True).decode("utf-8")

cmd = "uname -srm"
kernel = subprocess.check_output(cmd, shell=True).decode("utf-8")
# Write four lines of text.

draw.text((x, top+0), "Ramyad's Pi", fill=255)
draw.text((x, top+8), kernel, fill=255)
draw.text((x, top+16), "MAC:"+MAC, font=font, fill=255)
draw.text((x, top+24), "IP:"+IP, font=font, fill=255)

# Display image.
disp.image(image)
disp.show()
time.sleep(3)

draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.image(image)
disp.show()


#draw.rectangle((0, 0, width, height), outline=0, fill=0)

#draw.text((x, top), "IP: "+IP, fill=255)
#draw.text((x+5, top+16), "Humidity: %0.1f %%" % sensor.relative_humidity, fill=255)
#draw.text((x+5, top+24), "Temperature: %0.1f C" % sensor.temperature, fill=255)
#disp.image(image)
#disp.show()
#time.sleep(2)

#disp.image(image)
#disp.show()

