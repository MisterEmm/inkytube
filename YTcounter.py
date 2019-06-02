from inky import InkyPHAT
from time import sleep
import RPi.GPIO as GPIO
from PIL import Image, ImageFont, ImageDraw
import requests

# Set up the GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) # Notification LED
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Views/Subs Toggle Switch
GPIO.setwarnings(False)

# Set up the structure of the API request URL

URL = "https://www.googleapis.com/youtube/v3/channels"
type = "statistics"
channelid = "YOUR_CHANNEL_ID"
apikey = "YOUR_API_KEY"
PARAMS = {('part', type), ('id',channelid), ('key',apikey)}

# Set defaults for the Inky pHAT

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.RED)

# Infinite loop to query the YouTube API at regular intervals & display results on the Inky pHAT

while True:
    if (GPIO.input(24) == 1):
        print ("Subscribers Mode")
        GPIO.output(16,True) # Notification LED On
        r = requests.get(url = URL, params = PARAMS)
        data = r.json() # Store the API results in an object
        subscribers = data['items'][0]['statistics']['subscriberCount'] # Drill down into response and choose the right item
        totalviews = data['items'][0]['statistics']['viewCount']

        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)

        # Set the Inky background colour to Red
        
        for y in range(0, inky_display.HEIGHT):
            for x in range(0, inky_display.width):
                img.putpixel((x, y), inky_display.RED)
                
        # Define the fonts to use in the display        
    
        sfont = ImageFont.truetype('/home/pi/.fonts/Herkules.ttf', 110) # Or just use a standard font!
        vfont = ImageFont.truetype('/home/pi/.fonts/Herkules.ttf', 90)
        
        # Name the variables to display
        
        smessage = subscribers
        vmessage = totalviews
        
        # Set the co-ordinates for the text

        w, h = sfont.getsize(smessage)
        sx = (inky_display.WIDTH / 2) - (w / 2)
        sy = (inky_display.HEIGHT / 2) - (h / 1.6)
        
        # Display the combined background and text

        draw.text((sx, sy), smessage, inky_display.WHITE, sfont)
        inky_display.set_image(img)
        inky_display.show() # Display the new number
        sleep(3)
        GPIO.output(16,False) # Notification LED off
        sleep(1800) # Delay in seconds before refreshing

    else:
        print ("Views Mode") # Code the same as above just displaying vmessage (Views) instead of smessage (Subs)
        GPIO.output(16,True)
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        subscribers = data['items'][0]['statistics']['subscriberCount']
        totalviews = data['items'][0]['statistics']['viewCount']

        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
    
        for y in range(0, inky_display.HEIGHT):
            for x in range(0, inky_display.width):
                img.putpixel((x, y), inky_display.RED)
    
        sfont = ImageFont.truetype('/home/pi/.fonts/Herkules.ttf', 110)
        vfont = ImageFont.truetype('/home/pi/.fonts/Herkules.ttf', 90)

        smessage = subscribers
        vmessage = totalviews

        w, h = vfont.getsize(vmessage)
        sx = (inky_display.WIDTH / 2) - (w / 2)
        sy = (inky_display.HEIGHT / 2) - (h / 1.6)

        draw.text((sx, sy), vmessage, inky_display.WHITE, vfont)
        inky_display.set_image(img)
        inky_display.show()
        sleep(3)
        GPIO.output(16,False)
        sleep(600)

