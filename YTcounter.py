from inky import InkyPHAT
from time import sleep
import RPi.GPIO as GPIO
from PIL import Image, ImageFont, ImageDraw
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)

URL = "https://www.googleapis.com/youtube/v3/channels"
type = "statistics"
channelid = "YOUR_CHANNEL_ID"
apikey = "YOUR_API_KEY"
PARAMS = {('part', type), ('id',channelid), ('key',apikey)}

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.RED)



while True:
    if (GPIO.input(24) == 1):
        print ("Subscribers Mode")
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

        w, h = sfont.getsize(smessage)
        sx = (inky_display.WIDTH / 2) - (w / 2)
        sy = (inky_display.HEIGHT / 2) - (h / 1.6)

        draw.text((sx, sy), smessage, inky_display.WHITE, sfont)
        inky_display.set_image(img)
        inky_display.show()
        sleep(3)
        GPIO.output(16,False)
        sleep(1800)

    else:
        print ("Views Mode")
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

