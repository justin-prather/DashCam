import io
import time
import PIL, Image, ImageFont, ImageDraw
import picamera
import gps
import pytz
from pytz import reference
import datetime

localtime = reference.LocalTimezone()

session = gps.gps("localhost", "2947") 
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE) 

def time_adjust( s ):
	date = datetime.datetime.strptime( s, '%Y-%m-%dT%H:%M:%S.000z')
	date = date.replace(tzinfo=pytz.utc)
	date = date.astimezone(localtime)
	return date.strftime('%Y-%m-%d %H:%M:%S %Z')

print "Gathering data"
while True:
        try:
                report = session.next()
                # Wait for a 'TPV' report and display the current time 
                # To see all report data, uncomment the line below print 
                #print report
                if report['class'] == 'TPV':
                        if hasattr(report, 'time') & hasattr(report, 'lat') & hasattr(report, 'lon') & hasattr(report, 'alt'):
                                tim = time_adjust(report.time)
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
        camera.rotation = 180
        camera.resolution=(2592,1944)
        #camera.start_preview()
        time.sleep(5)
	camera.image_effect = 'cartoon'
        camera.capture(stream, format = 'jpeg' )

stream.seek(0)
image = Image.open(stream)

draw = ImageDraw.Draw(image)

ySize = image.size[1]

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 50)
draw.text( (20, ySize-(60*3)), "Time: " + str(tim), font=font, fill=(255, 0, 0)  )

draw.text( (20,ySize-(60*2)), "Position: " + str(lat) + ', ' + str(lon), font=font, fill=(255, 0, 0) )

draw.text( (20, ySize-(60*1)), "Altitude: " + str(alt), font=font, fill=(255, 0, 0)  )
del draw
image.save("ImageWithGPS_Data.jpg", "jpeg")
