import io
import time
import PIL, Image, ImageFont, ImageDraw
import picamera
import gps

session = gps.gps("localhost", "2947") 
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE) 

print "Gathering data"
while True:
	try:
		report = session.next()
		# Wait for a 'TPV' report and display the current time 
		# To see all report data, uncomment the line below print 
		#print report
		if report['class'] == 'TPV':
			if hasattr(report, 'time') & hasattr(report, 'lat') & hasattr(report, 'lon') & hasattr(report, 'alt'):
				tim = report.time
				lat = report.lat
				lon = report.lon
				alt = report.alt
				break
	except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print "GPSD has terminated"

print 'Data aquired, now capturing image'
stream = io.BytesIO()

with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(5)
	camera.capture(stream, format = 'jpeg' )

stream.seek(0)
image = Image.open(stream)

draw = ImageDraw.Draw(image)

xSize = image.size[0]

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 40)
draw.text( (xSize - 20,(50*3)), "Time: " + str(tim), font=font )

draw.text( (xSize - 20,(50*2)), "Position: " + str(lat) + ', ' + str(lon), font=font )

draw.text( (xSize - 20,(50*1)), "Altitude: " + str(alt), font=font )
del draw
image.save("ImageWithGPS_Data.jpg", "jpeg")
