import pygame
from pygame.locals import *
import gps
import sys
import os
import datetime
import pytz
from pytz import reference

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

climb = 0

localtime = reference.LocalTimezone()

session = gps.gps("localhost", "2947" )
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE )

pygame.init()
pygame.mouse.set_visible(False)

white = (255,255,255)
purple = (255, 0, 255)
red = (255,0,0)
black = (0,0,0)

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill(black)

#text = pygame.font.Font('freesansbold.ttf', 20)
font = pygame.font.Font('freesansbold.ttf', 20)

def write(text, pos, color):
	label = font.render(text, 1, color)
	screen.blit(label, pos)

write( "Waiting for GPS lock", (30,30), red )
while True:
	for event in pygame.event.get():
		if(event.type is MOUSEBUTTONDOWN):
			pygame.quit()
			sys.exit()
	report = session.next()
   	# Wait for a 'TPV' report and display the current time 
    	#see all report data, uncomment the line below print 
     	#print report
   	if report['class'] == 'TPV':
    	if hasattr(report, 'time'):
       		try:
				date = datetime.datetime.strptime( report.time, 
					'%Y-%m-%dT%H:%M:%S.000z')
			except:
				pass
			date = date.replace(tzinfo=pytz.utc)
			date = date.astimezone(localtime)
			try:
				date_s = date.strftime('%Y-%m-%d %H:%M:%S %Z')
      		except:
				pass
			
		if hasattr(report, 'lat'):	
			lat = report.lat
      	
      	if hasattr(report, 'lon'):	
      		lon = report.lon
      	if hasattr( report, 'alt'):
    		alt = report.alt
    	if hasattr( report, 'speed' ):
			speed = report.speed * gps.MPS_TO_KPH
		if hasattr( report, 'climb'):
			climb = report.climb * gps.MPS_TO_KPH
		
		if speed != 0:
			grade = 100 * (abs(climb)/speed)
		else:
			grade = 0

		try:
			screen.fill(black)
			write( date_s, (30,10), red )
			write( 'Latitude: '+ str(lat), (30,40), red )
			write( 'Longitude: ' + str(lon), (30,70), red )
			write( 'Altitude: ' + str(alt) + ' m', (30,100), red )
			write( 'Speed: ' + str(speed) + ' km/h', (30,130), red )
			write( 'Climb: ' + str(climb) + ' km/h', (30,160), red )			
			write( 'Grade: ' + str(grade) + ' %', (30,190), red )
		except:
			pass
	pygame.display.update()
