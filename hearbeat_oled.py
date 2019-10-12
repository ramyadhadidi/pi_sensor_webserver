import time

import board 
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
#disp.fill(0)
#disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((width-2, 0, width, 2), outline=0, fill=0)
    disp.image(image)
    disp.show()
    time.sleep(0.6)
    draw.rectangle((width-2, 0, width, 2), outline=0, fill=1)
    disp.image(image)
    disp.show()

