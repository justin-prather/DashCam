import gps
import pytz
from pytz import reference
import datetime

localtime = reference.LocalTimezone()

session = gps.gps("localhost", "2947" )
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE )

while True:
	try:
		report = session.next()
		if report['class'] == 'TPV':
			if hasattr(report, 'time' ):
				date = datetime.datetime.strptime( report.time, 
					'%Y-%m-%dT%H:%M:%S.000z')
				date = date.replace(tzinfo=pytz.utc)
				newdate = date.astimezone(localtime)
				print newdate.strftime('%Y-%m-%d %H:%M:%S %Z')
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print 'gps done'
