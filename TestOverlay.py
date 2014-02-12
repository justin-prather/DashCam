import io
import time
import PIL, Image, ImageFont, ImageDraw
import picamera

stream = io.BytesIO()

with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(5)
	camera.capture(stream, format = 'jpeg' )

stream.seek(0)
image = Image.open(stream)

draw = ImageDraw.Draw(image)

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 30)
draw.text( (20,20), "Hello World", font=font )
del draw
image.save("ImageWithOverlay.jpg", "jpeg")

